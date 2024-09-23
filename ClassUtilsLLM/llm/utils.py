def format_subtopic(subtopic):
    formatted_subtopic = subtopic
    if '.' in subtopic:
        formatted_subtopic = subtopic[subtopic.index('.')+1:]
    if ' ' in subtopic[:4]:
        formatted_subtopic = subtopic[subtopic.index(' ')+1:]
    return formatted_subtopic

def docs2string(docs):
  documents_txt = ''
  for doc in docs:
    documents_txt += f'{doc}\n'
  return documents_txt