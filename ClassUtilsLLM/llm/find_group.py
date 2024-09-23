from .tasks import txt_find_group

import numpy as np
import re

def accumulatted_contains(txt,groups):
  """
  Function to calculate the '''similarity''' (it's not embedding) 
  between a list of strings and a txt that is the substring of some of them.
  
  Args:
    txt:str - substring of one of the list of strings
    groups:list[str] - list of strings
  
  Returns:
    :int - the index of the group with the most similarity with the txt
  """
  txt_cleared = re.sub(r'[^\w\s]', '', txt)

  contage_by_group = [0]*len(groups)
  for sublen in range(1,len(txt_cleared)):
    stop = 0
    sub_txt = txt_cleared[:sublen]
    for g in range(len(groups)):
      if contage_by_group[g] != -1:
        if sub_txt in groups[g]:
          contage_by_group[g] += 1
        else:
          contage_by_group[g]=-1
      else:
        stop+=1

    if stop==len(contage_by_group)-1:
      break
  return np.argmax(contage_by_group)

def itBelongs(doc,groups,llm_query,LLM_MAXCHAR_PER_REQ=None,task=None):
  """
  Extract top-n taxonomy from a list of documents
  
  Args:
    doc:str - a document
    groups:list[str] - os grupos ao qual o documento pode pertencer
    llm_query:func(str) - function that communicates with API
    task:func(str,str)->str [default = None] - the task function to find the group of the document.
      Example: lambda doc,groups: f'@DOC\n{doc}\n@GROUPS\n@TASK: Which group of @GROUPS do the @DOC belongs?'
      By default, check the 'txt_find_group' from task
  Returns:
    :int - the index of the group the txt belongs to
  """
  
  ## Construção da pergunta para a llm
  if task is None:
    llm_question = txt_find_group(doc,groups)
  else:
    llm_question = task(doc,groups)
  
  ## Achando o grupo
  output = llm_query(llm_question)
  output = '\n'.join(output)
  
  ## Achando a qual grupo pertence
  return accumulatted_contains(output,groups)