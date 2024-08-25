import json
import openai

def create_llm_query(llm_base,llm_key):
  """
  Function used to create a communication port function
  Args:
    llm_base - link to API
    llm_key - key to acess the API
  Returns:
    llm_query:func(str) - a function that communicates with API
      and returns your answer
  """
  def llm_query(text):
    openai.api_llm_key = llm_key
    openai.api_base = llm_base

    response = openai.ChatCompletion.create(
        model="openchat_3.5",
        messages = [{"role": "user", "content": text}]

    )
    s = response['choices'][0]['message']['content'].split("\n")

    return s
  return llm_query