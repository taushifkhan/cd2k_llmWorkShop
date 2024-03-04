# cd2k_llmWorkShop

Use of LLM for gene prioritization for gene modules involve in interferon.
As a part of workshop, we use 6 modules annotated as INF from bloodGen v3.

In total, 114 genes were scored for statements related INF (see ./param/) using GPT4-turbo and GPT4 models.
We use Azure API implemented by JaX-IT.

## How to run

You might need followings,

1. Environment. Use requirement.txt file to build your the python environment.
2. Gene List: see the template of gene list in `./data/`
3. Authentication: Fill-in credentials to use LLM model (get in contact IT)
4. setup run: can be done locally or can be launched in HPC (sumner- sbatch )
5. Output : the out put in a string of Json object. where genes-modelID were keys and statements are strings. One might use pattern recognition to extract scores. 


OR,
# Use docker implementation of this code:

`
docker run -p 8501:8501 takh/llmgene_workshop:feb15
`

You will see the app in the browser : http://0.0.0.0:8501 
