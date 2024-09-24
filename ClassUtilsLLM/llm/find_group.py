from .tasks import txt_find_group

import numpy as np
import re
import difflib

def group_similarity(txt, groups):
  """
  Function to calculate the '''similarity''' (it's not embedding) 
  between a list of strings and a txt that is the substring of some of them.
  
  Args:
    txt:str - substring of one of the list of strings
    groups:list[str] - list of strings
  
  Returns:
    :int - the index of the group with the most similarity with the txt
  """
  melhor_ratio = 0
  idx_melhor_match = None
  for i,texto in enumerate(groups):
      sequencias_similares = difflib.SequenceMatcher(None, texto, txt).get_matching_blocks()
      
      for subseq in sequencias_similares:
          start = subseq.a
          end = start + subseq.size
          subsequencia = texto[start:end]
          ratio = difflib.SequenceMatcher(None, subsequencia, B).ratio()
          
          if ratio > melhor_ratio:
              melhor_ratio = ratio
              idx_melhor_match = i
  
  return idx_melhor_match



def itBelongs(doc,groups,llm_query,task=None,verbose=False):
  """
  Extract top-n taxonomy from a list of documents
  
  Args:
    doc:str - a document
    groups:list[str] - os grupos ao qual o documento pode pertencer
    llm_query:func(str) - function that communicates with API
    task:func(str,str)->str [default = None] - the task function to find the group of the document.
      Example: lambda doc,groups: f'@DOC\n{doc}\n@GROUPS\n@TASK: Which group of @GROUPS do the @DOC belongs?'
      By default, check the 'txt_find_group' from task
    verbose:bool [default = False] - print crude llm response in terminal
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
  if verbose:
    print(f"llm_output: {output}")
  
  ## Achando a qual grupo pertence
  return group_similarity(output,groups)