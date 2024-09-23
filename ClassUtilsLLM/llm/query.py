import json
import openai
import requests

def create_llm_query(llm_base,llm_key,model,return_models=False):
  """
  Function used to create a communication port function
  Args:
    llm_base - link to API
    llm_key - key to acess the API
    return_models [default=False] - instead of returning llm_query, the function returns
      wich 'models' are available. I strongly suggest to use this if you don't known 
      the name of the field 'model' (check for the value of key 'data' of the returned json
      and then the 'ids' for each dict in the list)
  Returns:
    llm_query:func(str) - a function that communicates with API
      and returns your answer
  """
  
  if return_models:
      openai.api_llm_key = llm_key
      openai.api_key = llm_key
      openai.api_base = llm_base
      response = requests.get(f"{openai.api_base}/models", headers={
          "Authorization": f"Bearer {openai.api_key}"
      })
      if response.status_code == 200:
          return response.json()
      else:
          raise ConnectionError(f"Error - Connection error while doing requesting of models")
      
  else:
    def llm_query(text):      
        openai.api_llm_key = llm_key
        openai.api_key = llm_key
        openai.api_base = llm_base
        response = openai.ChatCompletion.create(
            model=model,
            messages = [{"role": "user", "content": text}]
        
        )
        s = response['choices'][0]['message']['content'].split("\n")
        
        return s
    return llm_query

def create_llm_request_query(api_url):
  """
  Function to create a function that connects via request
  
  api_url:str - the link to connect in the API
  
  Returns:
    llm_query:func(str) - a function that communicates with API
      and returns your answer. It will return a json format, so probably you 
      must identify the key/value tuple that you want, like 'generated_text'
      to catch the return of llm.
  """
  
  def llm_query(txt):
    response = requests.post(api_url, data=txt)
    if response.status_code == 200:
      return response.json()
    else:
      raise ConnectionError(f"Error - Connection error while doing requesting text: '{txt[:30]} ...'. response status: {response.status_code}")
  return llm_query