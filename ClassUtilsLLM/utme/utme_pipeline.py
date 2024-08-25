import pandas as pd
from utme.BinaryClassifier import BinaryClassifier
from utme.TaxonomyClassifier import TaxonomyClassifier
from utme.SubcategoryGenerator import SubcategoryGenerator




def utme_pipeline(df,indexes,taxonomy,context,utme_base,
                  expansion_sample_size=10,):
  """
  Function responsible for making a streamlined UTME pipeline.
  
  Args:
    df:pd.Dataframe - dataframe in which the utme will be taken
      --> in this dataframe, there must be a column called 'text'
    indexes:list[int] - list of indexes that the utme will act on
    context:str - context extracted with powerful llm
    utme_base - utme instance
    expansion_sample_size:int [default=10] - expansion scale used in the process
  
  Returns:
    df_filtered_level2:pd.Dataframe - dataframe that includes the columns:
      y_pred - relative to the prediction made by BinaryClassifier
      level1 - level1 prediction
      level2 - level2 prediction
  """
  # Filtra apenas os de interesse
  df_filtered = df.iloc[indexes]
  
  
  # Start BinaryClassifier to filter documents of interest
  bc = BinaryClassifier(utme_base, context)
  y_pred = bc.classify(df_filtered.text.to_list())
  df_filtered['y_pred'] = y_pred
  df_filtered = df_filtered[df_filtered.y_pred == 'YES']
  
  # Start TaxonomyClassifier to map documents to predefined categories (First Level)
  tc = TaxonomyClassifier(bc, taxonomy)
  taxonomy_pred = tc.classify(df_filtered.text.to_list())
  df_filtered['level1'] = taxonomy_pred
  df_filtered_level1 = df_filtered[~df_filtered.level1.str.contains('NONE')]
  if True:
    print(f" - o nível 1 de taxonomia foi completo. Quantidade de únicos do level1: {len(df_filtered_level1.level1.unique())}")

  # Perform Unsupervised Taxonomy Expansion (Second Level)
  L = []
  for category in df_filtered_level1.level1.unique():
      sg = SubcategoryGenerator(tc)
      df_category = df_filtered_level1[df_filtered_level1.level1 == category]

      # Generate subcategories for the selected category
      subcategories = sg.generate_subcategories(category, df_category.sample(expansion_sample_size, replace=True).text.to_list())

      # Classify documents using the expanded subcategories
      tc2 = TaxonomyClassifier(bc, subcategories)
      taxonomy_pred2 = tc2.classify(df_category.text.to_list())

      df_category['level2'] = taxonomy_pred2
      L.append(df_category)
  df_filtered_level2 = pd.concat(L)
  return df_filtered_level2