from .tasks import txt_resume_2merge,txt_resume_2common,txt_resume_2severer
from enum import Enum

def resume_2merge(crude_taxonomies,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=None):
  llm_txt = f"""
  @TAXONOMY: {crude_taxonomies}
  
  {txt_resume_2merge(n_taxonomy)}
  """
  
  if LLM_MAXCHAR_PER_REQ is not None:
        if len(llm_txt)>LLM_MAXCHAR_PER_REQ:
            ## Separa em 2 grupos de tamanhos iguais e faz recursão
            t1 = resume_2merge(crude_taxonomies[:int(len(crude_taxonomies)/2)], n_taxonomy,llm_query)
            t2 = resume_2merge(crude_taxonomies[int(len(crude_taxonomies)/2):], n_taxonomy,llm_query)
            sum_of_them = t1+"\n"+t2
            return resume_2merge(sum_of_them,n_taxonomy,llm_query)
  
  resumed_taxonomys = '\n'.join(llm_query(llm_txt))
  return resumed_taxonomys


def resume_2common(crude_taxonomies,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=None):
  llm_txt = f"""
  @TAXONOMY: {crude_taxonomies}
  
  {txt_resume_2common(n_taxonomy)}
  """
  
  if LLM_MAXCHAR_PER_REQ is not None:
    if len(llm_txt)>LLM_MAXCHAR_PER_REQ:
        ## Separa em 2 grupos de tamanhos iguais e faz recursãos
        t1 = resume_2common(crude_taxonomies[:int(len(crude_taxonomies)/2)], n_taxonomy,llm_query)
        t2 = resume_2common(crude_taxonomies[int(len(crude_taxonomies)/2):], n_taxonomy,llm_query)
        sum_of_them = t1+"\n"+t2
        return resume_2common(sum_of_them,n_taxonomy,llm_query)
  
  resumed_taxonomys = '\n'.join(llm_query(llm_txt))
  return resumed_taxonomys


def resume_2severer(crude_taxonomies,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=None):
  llm_txt = f"""
  @TAXONOMY: {crude_taxonomies}
  
  {txt_resume_2severer(n_taxonomy)}
  """
  
  if LLM_MAXCHAR_PER_REQ is not None:
    if len(llm_txt)>LLM_MAXCHAR_PER_REQ:
        ## Separa em 2 grupos de tamanhos iguais e faz recursãos
        t1 = resume_2severer(crude_taxonomies[:int(len(crude_taxonomies)/2)], n_taxonomy,llm_query)
        t2 = resume_2severer(crude_taxonomies[int(len(crude_taxonomies)/2):], n_taxonomy,llm_query)
        sum_of_them = t1+"\n"+t2
        return resume_2severer(sum_of_them,n_taxonomy,llm_query)
  
  resumed_taxonomys = '\n'.join(llm_query(llm_txt))
  return resumed_taxonomys


class methods(Enum):
  MERGE2 = 0
  COMMON2 = 1
  SEVERER2 = 2

def resume(taxonomies,llm_query,n_taxonomy,method=methods.SPLIT2,LLM_MAXCHAR_PER_REQ=None):
    if methods.MERGE2==method:
        return resume_2merge(taxonomies,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=LLM_MAXCHAR_PER_REQ)
    elif methods.COMMON2==method:
        return resume_2common(taxonomies,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=LLM_MAXCHAR_PER_REQ)
    elif methods.SEVERER==method:
        return resume_2severer(taxonomies,llm_query,n_taxonomy,LLM_MAXCHAR_PER_REQ=LLM_MAXCHAR_PER_REQ)
    else:
        raise ValueError("resume's method is invalid")