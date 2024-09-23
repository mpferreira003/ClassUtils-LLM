from .tasks import txt_find_group
def itBelongs(doc,groups,llm_query,LLM_MAXCHAR_PER_REQ=None,task=None):
  """
  Extract top-n taxonomy from a list of documents
  
  Args:
    doc:str - a document
    groups:list[str] - os grupos ao qual o documento pode pertencer
    llm_query:func(str) - function that communicates with API
    task:str [default = None] - the task to find the group of the document.
  Returns:
    output:str - llm's answer
  """
  
  if task is None:
    task_txt = txt_find_group
  else:
    task_txt = task
  ## Construção da pergunta para a llm
  llm_question = f"@DOCUMENT\n{doc}\n"
  llm_question+= f"@GROUP\n{'\n'.join([f'{i} - {groups[i]}' for i in range(len(groups))])}"
  llm_question+=  "\n\n @TASK: " + task_txt
  
  ## Extração da taxonomia
  output = llm_query(llm_question)
  return output
