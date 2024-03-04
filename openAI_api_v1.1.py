
# Modules
import sys, time, json
from openai import AzureOpenAI
import pandas as pd
import numpy as np
# import seaborn as sns
from tqdm import tqdm
import argparse

# get api informations

# reading auth dictionary
#auth = json.load(open("./param/authentication.json","r"))
auth = json.load(open("./param/auth.json","r")) # will use g4 credentials


client = AzureOpenAI(
  api_key = auth['api_key'],  
  api_version = auth["version"],
  azure_endpoint = auth['api_base']  # Your Azure OpenAI resource's endpoint value.
)

# reading parameters input
argParse = argparse.ArgumentParser()
argParse.add_argument("-p", "--param", help="file path to parameter file in JSON format")
argParse.add_argument("-g", "--genelist", help="file path to genelist csv file [col name :Genes]")
argParse.add_argument("-o", "--out", help="result file name in json [output.json]")


args = argParse.parse_args()
print("args=%s" % args)
print("args.param=%s" % args.param)
print("args.genelist=%s" % args.genelist)
print("args.out=%s" % args.out)

## process input argumants
param_dict = json.load(open(args.param,"r"))
geneList = pd.read_csv(args.genelist)
outJson  = open(args.out,"w")

modelID = auth["engine_g4"]


# create prompt
def createPrompt(gname,params):
    #copy prompt here"
    promptx_head = "provide following for the gene {} in json format: ".format(gname)
    prompt_body  = "{}, {}. {} in Json format with statement as key and score as value. ".format(params['background'][0],params['background'][1] ,params['scoring_strategy'])
    prompt_question_text = "\n".join(params['question'])
    promptx = promptx_head+prompt_body+prompt_question_text
    return promptx



def callGPT_completion(modelID,promptID, temperature_set):
    response = client.completions.create(
              model=modelID,
              prompt=promptID,
              temperature=temperature_set,
              max_tokens=1000,
              top_p=1.0,
              frequency_penalty=0.0,
              presence_penalty=0.0
            )

    if response.choices[0].finish_reason == "stop":
        return response.choices[0].text.split("\n")
    else:
        return 0
    
def callGPT_chatCompletion(modelID, prompt_x, temperature_set):
    response_chat = client.chat.completions.create(
                model=modelID,
                messages=[{"role":'system',"content":prompt_x}],
                temperature=temperature_set,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0)

    if response_chat.choices[0].finish_reason == "stop":
        return response_chat.choices[0].message.content.split("\n")
    else:
        return 0



def run_for_gene(gname, param, engine, temperature=0.7, backofftimer = 40,iteration=1, mode="chat"):
    print (gname)
    pd_tmp = {}
    promptx = createPrompt(gname, param)

    for k in np.arange(1,1+iteration):
        start = time.time()
        if mode == "chat":
            res = callGPT_chatCompletion(engine,promptx,temperature)

        elif mode == "completion":
            res = callGPT_completion(engine, promptx, temperature)
        
        time.sleep(backofftimer)
        runID = "{}_{}".format(engine, k)
        pd_tmp[runID] = res

            
    return pd_tmp


dfAll = {}
run_temp = param_dict["model_setting"]["temperature"]
run_iteration = param_dict["model_setting"]["q_iter"]

for k in tqdm(geneList['Gene Symbol'].values):
    #start = time.time()
    dxv = run_for_gene(k,param_dict, modelID, mode="chat", backofftimer=30,iteration=run_iteration,temperature=run_temp)
    #end = time.time()
    #if end-start < 50:
    #    time.sleep(50)
    dfAll[k] = dxv

# save out put in json
json.dump(dfAll,outJson,indent=4)
