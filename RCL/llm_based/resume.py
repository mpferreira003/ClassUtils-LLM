from .tasks import txt_resume_2merge, txt_resume_2common, txt_resume_2severer
from enum import Enum

def resume_2merge(crude_taxonomies, llm_query, n_taxonomy, LLM_MAXCHAR_PER_REQ=None):
  """
  Type of summary that uses the 'txt_resume_2merge' task, available in tasks.py.
  
  Args:
    crude_taxonomies: list[str] - full list of taxonomies.
    llm_query: func(str) - function that sends prompts to the LLM and returns the response.
    n_taxonomy: int - number of taxonomies to be generated.
    LLM_MAXCHAR_PER_REQ: int [default=None] - integer that determines the maximum character 
      capacity per request to the LLM. If the text size exceeds this limit, the request 
      is split into two. If this parameter is None, the request is never split.
  
  Returns:
    resumed_taxonomys: str - string containing the final list of generated taxonomies.
  """
  llm_txt = f"""
  @TAXONOMY: {crude_taxonomies}
  
  {txt_resume_2merge(n_taxonomy)}
  """
  
  if LLM_MAXCHAR_PER_REQ is not None:
        if len(llm_txt) > LLM_MAXCHAR_PER_REQ:
            ## Splits into 2 equal-sized groups and recurses
            t1 = resume_2merge(crude_taxonomies[:int(len(crude_taxonomies)/2)], n_taxonomy, llm_query)
            t2 = resume_2merge(crude_taxonomies[int(len(crude_taxonomies)/2):], n_taxonomy, llm_query)
            sum_of_them = t1 + "\n" + t2
            return resume_2merge(sum_of_them, n_taxonomy, llm_query)
  
  resumed_taxonomys = '\n'.join(llm_query(llm_txt))
  return resumed_taxonomys


def resume_2common(crude_taxonomies, llm_query, n_taxonomy, LLM_MAXCHAR_PER_REQ=None):
  """
  Type of summary that uses the 'txt_resume_2common' task, available in tasks.py, 
  which focuses on obtaining the most frequent taxonomies (e.g., "get the 7 most 
  frequent taxonomies").
  
  Args:
    crude_taxonomies: list[str] - full list of taxonomies.
    llm_query: func(str) - function that sends prompts to the LLM and returns the response.
    n_taxonomy: int - number of taxonomies to be generated.
    LLM_MAXCHAR_PER_REQ: int [default=None] - integer that determines the maximum character 
      capacity per request to the LLM. If the text size exceeds this limit, the request 
      is split into two. If this parameter is None, the request is never split.
  
  Returns:
    resumed_taxonomys: str - string containing the final list of generated taxonomies.
  """
  llm_txt = f"""
  @TAXONOMY: {crude_taxonomies}
  
  {txt_resume_2common(n_taxonomy)}
  """
  
  if LLM_MAXCHAR_PER_REQ is not None:
    if len(llm_txt) > LLM_MAXCHAR_PER_REQ:
        ## Splits into 2 equal-sized groups and recurses
        t1 = resume_2common(crude_taxonomies[:int(len(crude_taxonomies)/2)], n_taxonomy, llm_query)
        t2 = resume_2common(crude_taxonomies[int(len(crude_taxonomies)/2):], n_taxonomy, llm_query)
        sum_of_them = t1 + "\n" + t2
        return resume_2common(sum_of_them, n_taxonomy, llm_query)
  
  resumed_taxonomys = '\n'.join(llm_query(llm_txt))
  return resumed_taxonomys


def resume_2severer(crude_taxonomies, llm_query, n_taxonomy, LLM_MAXCHAR_PER_REQ=None):
  """
  Type of summary that uses the 'txt_resume_2severer' task, available in tasks.py. 
  This type of summary prioritizes asking for the taxonomies that the LLM considers 
  most important.
  
  Args:
    crude_taxonomies: list[str] - full list of taxonomies.
    llm_query: func(str) - function that sends prompts to the LLM and returns the response.
    n_taxonomy: int - number of taxonomies to be generated.
    LLM_MAXCHAR_PER_REQ: int [default=None] - integer that determines the maximum character 
      capacity per request to the LLM. If the text size exceeds this limit, the request 
      is split into two. If this parameter is None, the request is never split.
  
  Returns:
    resumed_taxonomys: str - string containing the final list of generated taxonomies.
  """
  llm_txt = f"""
  @TAXONOMY: {crude_taxonomies}
  
  {txt_resume_2severer(n_taxonomy)}
  """
  
  if LLM_MAXCHAR_PER_REQ is not None:
    if len(llm_txt) > LLM_MAXCHAR_PER_REQ:
        ## Splits into 2 equal-sized groups and recurses
        t1 = resume_2severer(crude_taxonomies[:int(len(crude_taxonomies)/2)], n_taxonomy, llm_query)
        t2 = resume_2severer(crude_taxonomies[int(len(crude_taxonomies)/2):], n_taxonomy, llm_query)
        sum_of_them = t1 + "\n" + t2
        return resume_2severer(sum_of_them, n_taxonomy, llm_query)
  
  resumed_taxonomys = '\n'.join(llm_query(llm_txt))
  return resumed_taxonomys


class methods(Enum):
  MERGE2 = 0
  COMMON2 = 1
  SEVERER2 = 2

def resume(taxonomies, llm_query, n_taxonomy, method=methods.MERGE2, LLM_MAXCHAR_PER_REQ=None):
    """
  Default function that uses the resume.methods enum to select the method used.
  
  Args:
    taxonomies: list[str] - full list of taxonomies.
    llm_query: func(str) - function that sends prompts to the LLM and returns the response.
    n_taxonomy: int - number of taxonomies to be generated.
    LLM_MAXCHAR_PER_REQ: int [default=None] - integer that determines the maximum character 
      capacity per request to the LLM. If the text size exceeds this limit, the request 
      is split into two. If this parameter is None, the request is never split.
    method: methods - method used to perform the summary.
  
  Returns:
    resumed_taxonomys: str - string containing the final list of generated taxonomies.
  """
    if methods.MERGE2 == method:
        return resume_2merge(taxonomies, llm_query, n_taxonomy, LLM_MAXCHAR_PER_REQ=LLM_MAXCHAR_PER_REQ)
    elif methods.COMMON2 == method:
        return resume_2common(taxonomies, llm_query, n_taxonomy, LLM_MAXCHAR_PER_REQ=LLM_MAXCHAR_PER_REQ)
    elif methods.SEVERER2 == method:
        return resume_2severer(taxonomies, llm_query, n_taxonomy, LLM_MAXCHAR_PER_REQ=LLM_MAXCHAR_PER_REQ)
    else:
        raise ValueError("resume's method is invalid")
