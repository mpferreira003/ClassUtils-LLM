"""
File that controls que texts used to send prompts to the llm
"""


## taxonomy prompts
txt_get_taxonomy = lambda documents,n_taxonomy: f'@DOCUMENTS\n{documents}\n\n@TASK: Generate the top-{n_taxonomy} topics using the content from @DOCUMENTS. The output must be listed and enumerated.'


## resume prompts
txt_resume_2merge = lambda n_taxonomy: f'Merge the context from @TAXONOMY into a top-{n_taxonomy} list. The output must be listed and enumerated.'
txt_resume_2common = lambda n_taxonomy: f'create a top-{n_taxonomy} list with the most-common items in @TAXONOMY. The output must be listed and enumerated.'
txt_resume_2severer = lambda n_taxonomy: f'create a top-{n_taxonomy} list with the severer items in @TAXONOMY. The output must be listed and enumerated.'


## context prompts
txt_context_summarize = 'Summarize the @TAXONOMY into a comprehensive topic, in a few words'

## find group prompts
def txt_find_group(doc,groups):
    llm_question = f"@DOCUMENT\n{doc}\n"
    llm_question+= "@GROUP\n{}".format('\n'.join([f'{i} - {groups[i]}' for i in range(len(groups))]))
    llm_question+=  "\n\n @TASK: " + "Choose one of the group's id from @GROUP that has most similarity between @DOCUMENT. Just show it in the terminal, don't answer nothing more"
    return llm_question