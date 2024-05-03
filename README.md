# cd2k_llmWorkShop

Use of LLM for gene prioritization for gene modules involve in interferon.
As a part of workshop, we use 6 modules annotated as IFN from bloodGen v3.

In total, 114 genes were scored for statements related IFN (see ./param/) using GPT4-turbo and GPT4 models.
We use Azure API implemented by JaX-IT.

## How to run

You might need followings,

1. Environment. Use requirement.txt file to build your the python environment.
2. Gene List: see the template of gene list in `./data/`
3. Authentication: Fill-in credentials to use LLM model (see ``./param/auth.json``)
4. setup run: 

```bash
code % python openAI_api_v1.1.py --help
usage: openAI_api_v1.1.py [-h] [-p PARAM] [-g GENELIST] [-o OUT]

optional arguments:
  -h, --help            show this help message and exit
  -p PARAM, --param PARAM
                        file path to parameter file in JSON format
  -g GENELIST, --genelist GENELIST
                        file path to genelist csv file [col name :Genes]
  -o OUT, --out OUT     result file name in json [output.json]
```

5. Output : the out put in a string of Json object. where genes-modelID were keys and statements are strings. One might use pattern recognition to extract scores. 


OR,
# Use docker implementation of this code:

`
docker run -p 8501:8501 takh/llmgene_workshop:latest
`

You will see the app in the browser : http://0.0.0.0:8501 
