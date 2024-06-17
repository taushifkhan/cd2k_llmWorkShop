import streamlit as st
import numpy as np
import pandas as pd
from glob import glob
import json, time, sys

sys.path.append("app_dev/codeBase")
import openAI_api_withwait as oX

st.set_page_config(page_title="Try BloodGen3 Modules", page_icon=":bow_and_arrow:")

st.markdown("""
#### Use gene list from BloodGen3 Repo [left column] to explore themes [right column].
""")
bloodGen3 = pd.read_csv("app_dev/data_repo/geneList/ModuleTranscript_BioINfo.csv")

param_theme_dir = 'app_dev/data_repo/paramFiles/'
param_theme={'erythropoiesis':param_theme_dir+'erythropoiesis_param.json',\
             'Interferone':param_theme_dir+'ifn_workshop.json',\
             'DiseaseSp_Sepsis':param_theme_dir+'sepsis_param.json',\
            'TNBC_geneAssocation_Test':param_theme_dir+'tnbc_GeneAssociation_step1.json',\
            'TNBC_geneAction_Test':param_theme_dir+'tnbc_GeneAction_step2.json',\
            'TNBC_geneFunction_Test':param_theme_dir+'tnbc_GeneMode_step3.json'}

module_selection, paramFile_selection = st.columns(2)

with module_selection:
    st.header("Select gene modules")
    q_title = st.selectbox("Selection Module based on Annotation", sorted(list(bloodGen3['Module title'].unique())))
    s_module = st.selectbox("Select module id:", list(bloodGen3[bloodGen3['Module title']==q_title]["ID"].values))

    if q_title and s_module:
        genes_selected = list(set([i.strip() for i in bloodGen3[bloodGen3["ID"] == s_module]["Member genes"].values[0].split(",")]))
        st.info("{} module {} has {} genes".format(q_title, s_module, len(genes_selected)))
        with st.expander("see genes in the moule"):
            st.write(",".join(genes_selected))

with paramFile_selection:
    st.header("Select parameter based on theme")
    param_select = st.selectbox("choose param JSON:", list(param_theme.keys()))
    param_json_x   = json.load(open(param_theme[param_select],"r"))
    with st.expander("see parameter file"):
        st.json(param_json_x)

st.sidebar.header("LLM Progress")
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

st.warning("current version works best with GPT4 models")

# calling authenticator before procceding
if 'api_obj' not in st.session_state:
    st.warning("To proceed further activate sesson with key")
    st.stop()
else:
    callAPI = st.session_state['api_obj']

openAi_models_sel = callAPI.modelInfo[(callAPI.modelInfo.modelName.str.contains("gpt"))&(callAPI.modelInfo.ownedby=="openai")]
openAi_models_select = st.selectbox("Select Model [gpt engine]",list(openAi_models_sel.modelName.values))
st.info("prompt will use selected model : {}".format(openAi_models_select))

with st.form("run_bloodgen3"):
    gene_to_run_count = st.slider(label="choose (n) top gene:", min_value=2,max_value=len(genes_selected))
    st.info("Will use top {}[/{}] gene from the list".format(gene_to_run_count, len(genes_selected)))
    submitted_p3 = st.form_submit_button("Generate Response [~ 1 mins/ gene]",use_container_width=True)
    json_response = {}
    gen_to_run = genes_selected[:gene_to_run_count]

    if submitted_p3:
        st.write("Genrating LLM response ...[Approximate time for {} genes ~ {} cpu mins]".format(gene_to_run_count,gene_to_run_count))
        time_start = time.time()
        last_run = 0
        for i in range(1, len(gen_to_run)+1):
            status_text.text("Runnning for {} [{}/{}]| last run {}sec".format(gen_to_run[i-1], i, gene_to_run_count, last_run))
            dxv = oX.run_for_gene(callAPI, gen_to_run[i-1],param_json_x, model_to_use= openAi_models_select, backofftimer = 40,iteration=1)
            json_response[gen_to_run[i-1]] = dxv
            last_run = round(time.time()-time_start,2)
            progress_bar.progress(int(i/(len(gen_to_run)+1)*100))
            
        total_time = round(time.time()-time_start,2)
        st.write("completed in {} sec [{} mins]".format(total_time, round(total_time/60),2))

progress_bar.empty()

if json_response:
    st.info("Save output as JSON file")
    json_string_response = json.dumps(json_response)
    with st.expander("Response in JSON:"):
        st.write(json_response)
    st.download_button(
        label="Download JSON",
        file_name="{}_{}_geneLLM.json".format(q_title,s_module).replace(" ",""),
        mime="application/json",
        data=json_string_response,
    )

    # try:
    #     csvDF = pd.DataFrame.from_dict(json_string_response)
    #     st.write("Response score as CSV")
    #     st.write(csvDF)
    # except:
    #     pass

    # # st.info("Response as CSV")
    # # outCSV = oX.convertJson_DF(json_response)
    # # st.write(outCSV.T)
    # # st.download_button(
    # #     label="Download data as CSV",
    # #     data=outCSV.to_csv().encode('utf-8'),
    # #     file_name='LLM_reponse_{}_{}.csv'.format(s_module,param_select),
    # #     mime='text/csv',    
    # #     )
