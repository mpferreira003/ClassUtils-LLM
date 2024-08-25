## Motivação

Este projeto foi desenvolvido através de um projeto de pesquisa em llms em conjunto ao laboratório [Labic](https://labic.icmc.usp.br). 
O foco é resolver o problema de processamento em grandes conjuntos textuais com técnicas baseadas em _clustering_.

## Instalando a ferramenta

A ferramenta foi desenvolvida para funcionar como uma biblioteca python, então é possível instalá-la fazendo:

```
git clone https://github.com/mpferreira003/RCL.git
pip install RCL/
```

Dentro do projeto, existe uma pasta _examples_, que possui notebooks para a demonstração do uso da ferramenta.

## Funcionalidades

O projeto conta com 3 pacotes principais:
- amostragem
- funções de llm
- predição

A amostragem pode ser conferida em 'sampling.py' e incluí funções responsáveis por selecionar dados específicos em um conjunto, em geral a partir de métodos de clustering.

As funções disponíveis para a llm estão contidas na pasta 'llm_based'. Para se conectar via API usa-se a função disponível em 'query.py'. Para realizar tarefas de taxonomia e contexto, pode-se usar usar os respectivos arquivos. Caso seja necessária alguma alteração nos prompts, acesse 'tasks.py'

Existe também o arquivo 'norm.py', feito para suportar métodos de normalização de conjuntos de dados.

## Etapa atual

Os preditores já funcionam parcialmente, porém eles ainda não estão implementados a pontos de funcionarem com o pipeline.