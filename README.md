# Classification Utils by LLM
## Motivation

This project was developed as part of a research project on LLMs in collaboration with the [LABIC-ICMC-USP](https://labic.icmc.usp.br) laboratory. The focus is on solving the problem of processing large textual datasets using clustering-based techniques.

## Installing the Tool

The tool was developed to function as a Python library, so it can be installed using:
```
git clone https://github.com/mpferreira003/RCL.git pip install RCL/
```

Within the project, there is an `examples` folder containing notebooks that demonstrate the use of the tool.

## Features

The project has three main packages:
- Sampling
- LLM Functions
- Prediction

Sampling can be found in `sampling.py` and includes functions responsible for selecting specific data from a dataset, generally using clustering methods.

The available LLM functions are contained within the `llm_based` folder. To connect via API, use the function available in `query.py`. To perform taxonomy and context tasks, you can use the respective files. If any changes to prompts are necessary, refer to `tasks.py`.

There is also the `norm.py` file, created to support dataset normalization methods.

## Current Stage

The predictors are partially functional, but they are not yet implemented to work fully with the pipeline.
