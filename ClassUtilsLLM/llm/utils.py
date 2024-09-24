def format_subtopic(subtopic):
    formatted_subtopic = subtopic
    if '.' in subtopic:
        formatted_subtopic = subtopic[subtopic.index('.')+1:]
    if ' ' in subtopic[:4]:
        formatted_subtopic = subtopic[subtopic.index(' ')+1:]
    return formatted_subtopic

def docs2string(docs):
  documents_txt = ''
  for i,doc in enumerate(docs):
    documents_txt += f'Document{i}: {doc}\n'
  return documents_txt