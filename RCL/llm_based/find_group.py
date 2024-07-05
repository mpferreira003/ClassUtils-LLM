from .utils import docs2string
from .tasks import txt_find_group
from enum import Enum
def itBelongs(doc,groups,llm_query,LLM_MAXCHAR_PER_REQ=None):
  """
  Extract top-n taxonomy from a list of documents
  
  Args:
  doc - string: a document
  groups - list[str]: os grupos ao qual o documento pode pertencer
  llm_query - (function): function to answer NLP questions (like LLM API)
  """
  
  ## Construção da pergunta para a llm
  llm_question = f"@DOCUMENT\n{doc}\n" + \
                 f"@GROUP\n{'\n'.join([f'{i} - {groups[i]}' for i in range(len(groups))])}" + \
                 "\n\n===\n" + txt_find_group
  
  ## Extração da taxonomia
  output = llm_query(llm_question)
  return output
