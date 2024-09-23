"""
File that controls que texts used to send prompts to the llm
"""


## taxonomy prompts
txt_get_taxonomy = lambda documents,n_taxonomy: '@DOCUMENTS\n{documents}\n\n@TASK: Generate the top-{n_taxonomy} topics using the content from @DOCUMENTS. The output must be listed and enumerated.'


## resume prompts
txt_resume_2merge = lambda n_taxonomy: 'Merge the context from @TAXONOMY into a top-{n_taxonomy} list. The output must be listed and enumerated.'
txt_resume_2common = lambda n_taxonomy: 'create a top-{n_taxonomy} list with the most-common items in @TAXONOMY. The output must be listed and enumerated.'
txt_resume_2severer = lambda n_taxonomy: 'create a top-{n_taxonomy} list with the severer items in @TAXONOMY. The output must be listed and enumerated.'


## context prompts
txt_context_summarize = 'Summarize the @TAXONOMY in a context paragraph, using short expressions and keywords. Remove 0 NONE.'

## find group prompts
txt_find_group = "Choose one of the group's id from @GROUP that has most similarity between @DOCUMENT"