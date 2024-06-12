import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="About", page_icon=":eyeglasses:")

st.markdown("""
### Related Articles:
            
1. Automating Candidate Gene Prioritization with Large Language Models: Development and Benchmarking of an API-Driven Workflow Leveraging GPT-4. [in-preparation]
2. Toufiq M, Rinchai D, Bettacchioli E, Kabeer BSA, Khan T, Subba B, et al. Harnessing large language models (LLMs) for candidate gene prioritization and selection. J Transl Med. 2023;21(1):728. https://doi.org/10.1186/s12967-023-04576-8
3. Rinchai D, Altman MC, Konza O, Hässler S, Martina F, Toufiq M, et al. Definition of erythroid cell‑positive blood transcriptome phenotypes associated with severe respiratory syncytial virus infection. Clin Transl Med. 2020;10(8):e244.
4. Rinchai D, Chaussabel D. A training curriculum for retrieving, structuring, and aggregating information derived from the biomedical literature and large‑scale data repositories. F1000Research. 2022. https://doi.org/10.12688/f1000research.122811.1.
5. Altman MC, Rinchai D, Baldwin N, Toufiq M, Whalen E, Garand M, et al. Development of a fixed module repertoire for the analysis and interpretation of blood transcriptome data. Nat Commun. 2021;12(1):4385.
     
### Where to find:
1. code base = https://github.com/taushifkhan/cd2k_llmWorkShop.git
2. docker hub = https://hub.docker.com/repository/docker/takh/llmgene_workshop

### How to Run Docker Container:

Follow these steps to run a Docker container using the `takh/llmgene_workshop:latest` image:

#### 1. Install Docker

Ensure Docker is installed on your system. Download it from the 
[Docker website](https://www.docker.com/products/docker-desktop) and follow the installation instructions for your operating system.

#### 2. Pull a Docker Image

Before running a container, you need to have a Docker image. Pull the image from Docker Hub with the following command:

```bash
docker pull takh/llmgene_workshop:latest # to get the container
docker run -p 8501:8501 takh/llmgene_workshop:latest # run locally application is on localhost:8501
            
docker stop [container-id or name] # stop application
docker start [container-id or name] # start
docker rm [container-id or name]    # remove the container    
```
            
### Without Docker application

Download the python script from (git repo)[https://github.com/taushifkhan/cd2k_llmWorkShop.git]. Set up authentication keys in ./param/auth.json and run with gene list. 
User can change the promot in presecribed format as shown in (param) directory .
            
Upon successful installation of requirements and creation onf virtual environment, use folllowing comad to check the code
            
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

### How to get private API key:
API key can be obtained from openAI website. Read more [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
            
### How to get Azure API key: 
You might have to contact your IT team. Or read more [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-studio)

""")