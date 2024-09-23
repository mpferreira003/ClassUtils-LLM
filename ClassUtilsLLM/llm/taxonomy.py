from .utils import docs2string
from .tasks import txt_get_taxonomy
from enum import Enum
def taxonomy_2split(docs,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=None,task=None):
  """
  Extract top-n taxonomy from a list of documents
  
  Args:
    docs:list[string] - list of documents to extract the taxonomy
    llm_query:func(str) - function that communicates with API
    n_taxonomy:int - quantity of taxonomy that would be generated
    task:func(str,str)->str [default = None] - may receive a function that 
      returns the prompt to llm. 
      Example: task=lambda docs,n: f'documents:\n{docs}\n\n task: tell me how many taxonomies are in the documents.'
      By default, the prompt is given by the 'txt_get_taxonomy' function in tasks.py 
  Returns:
    taxonomy:str - contains a list of the generated taxonomies
  """
  
  ## Construção da pergunta para a llm
  documents_txt = docs2string(docs)
  if task is None:
    llm_question = txt_get_taxonomy(documents_txt,n_taxonomy)
  else:
    llm_question = task(documents_txt,n_taxonomy)
  
  if LLM_MAXCHAR_PER_REQ is not None:
    if len(llm_question)>LLM_MAXCHAR_PER_REQ:
        ## Separa em 2 grupos de tamanhos iguais e faz recursão
        
        t1 = taxonomy_2split(docs[:int(len(docs)/2)], llm_query,n_taxonomy)
        t2 = taxonomy_2split(docs[int(len(docs)/2):], llm_query,n_taxonomy)
        return t1+"\n"+t2
  
  
  ## Extração da taxonomia
  output = llm_query(llm_question)
  taxonomy = '0 NONE'
  for item in output:
    v = item.split('.')
    if len(v) >= 2:
      if v[0].isnumeric(): taxonomy += "\n"+item.strip()
  return taxonomy

class methods(Enum):
  SPLIT2 = 0

def taxonomy(docs,llm_query,n_taxonomy,method=methods.SPLIT2,**kwargs):
    """
    Main function for taxonomy extraction
    Args:
      docs:list[string] - list of documents to extract the taxonomy
      llm_query:func(str) - function that communicates with API
      n_taxonomy:int - quantity of taxonomy that would be generated
      method:methods [default = methods.SPLIT2] - choosed method
    Returns:
      taxonomy:str - contains a list of the generated taxonomies
    """
    if methods.SPLIT2==method:
        return taxonomy_2split(docs,llm_query,n_taxonomy,**kwargs)
    else:
        raise ValueError("taxonomy's method is invalid")