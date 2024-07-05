from .utils import docs2string
from .tasks import txt_get_taxonomy
from enum import Enum
def taxonomy_2split(docs,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=None):
  """
  Extract top-n taxonomy from a list of documents
  
  Args:
  docs - (list[string]): list of documents to extract the taxonomy
  n_taxonomy - (int): quantity of taxonomy that would be generated
  llm_query - (function): function to answer NLP questions (like LLM API)
  """

  ## Construção da pergunta para a llm
  documents_txt = docs2string(docs)
  task = txt_get_taxonomy(n_taxonomy)
  llm_question = documents_txt + "\n\n===\n" + task
  
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

def taxonomy(docs,llm_query,n_taxonomy,method=methods.SPLIT2):
    if methods.SPLIT2==method:
        return taxonomy_2split(docs,llm_query,n_taxonomy)
    else:
        raise ValueError("taxonomy's method is invalid")