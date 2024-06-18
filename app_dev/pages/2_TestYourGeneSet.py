import streamlit as st
import numpy as np
import pandas as pd
import json, time, sys

sys.path.append("app_dev/codeBase")
import openAI_api_withwait as oX

    
def _checkParamFile(param_json):
    if all(key in param_json for key in ('background', 'scoring_strategy', 'question')):
        st.info("Parameters are defined")
        return True
    else:
        st.warning("Parameters are not defined")
        return False

example_gene_file = "app_dev/data_repo/demo/M9.2_genes.csv"
example_param_file = "app_dev/data_repo/demo/test_param.json"


st.set_page_config(page_title="Upload your gene set", page_icon="📈")

st.markdown("""
## Use following parameters to examine your gene set.
**Important** : For long list of genes consider using local deployment
""")

gene_upload, paramFile_upload = st.columns(2)

with gene_upload:
    uploaded_gene_file = st.file_uploader("Choose a CSV file with genes in 'Genes' column",type=['csv'])
    load_Exmaple_gene = st.checkbox("Load Example gene list")

    if uploaded_gene_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        gene_dataframe = pd.read_csv(uploaded_gene_file)
        if 'Genes' in gene_dataframe.columns:
            st.info("Gene list uploaded")
            st.write(gene_dataframe)
        else:
            st.warning("Consider renaming gene coulumn as 'Genes'. Can not process uploaded file")
            gene_dataframe = pd.DataFrame()

    elif load_Exmaple_gene:
        gene_dataframe = pd.read_csv(example_gene_file)
        st.info("Loading example gene file.")
        st.write(gene_dataframe)
    else:
        st.warning("Please upload gene list")

with paramFile_upload:

    uploaded_param_file = st.file_uploader("Choose a JSON file with DEFINED paramters",type=['json'])
    load_example_params = st.checkbox("Load example parameters")

    if uploaded_param_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        param_json = json.load(uploaded_param_file)
        assert _checkParamFile(param_json)
        st.json(param_json)
        
    elif load_example_params:
        st.info("Loading example parameters file.")
        with open(example_param_file) as f:
            param_json = json.load(f)
        assert _checkParamFile(param_json)
        st.json(param_json)
    else:
        st.warning("Please upload parameter file")

if 'api_obj' not in st.session_state:
        st.warning("To proceed further activate sesson with key")
else:
    callAPI = st.session_state['api_obj']
    st.info("API object is active")
    openAi_models_sel = callAPI.modelInfo[(callAPI.modelInfo.modelName.str.contains("gpt"))&(callAPI.modelInfo.ownedby=="openai")]
    openAi_models_select = st.selectbox("Select Model [gpt engine]",list(openAi_models_sel.modelName.values))
    st.info("prompt will use selected model : {}".format(openAi_models_select))

if gene_dataframe.empty or not param_json or 'api_obj' not in st.session_state:
    st.warning("Please upload gene list and parameters to proceed further")
    st.stop()
else:
    with st.form("Try_gene_set"):
        st.write("Upload your gene list and parameters to proceed further")
        st.write("Note: Gene list should be in CSV format with 'Genes' column")
        st.write("Note: Parameters should be in JSON format with 'background', 'scoring_strategy' and 'question' keys")
        
        gene_to_run_count = st.slider(label="choose n top gene:", min_value=2,max_value=gene_dataframe.Genes.nunique())
        st.info("Will use top {}[/{}] gene from the uploaded doc".format(gene_to_run_count, gene_dataframe.Genes.nunique()))
        gList = gene_dataframe.Genes.values
        gen_to_run = gList[:gene_to_run_count]
        
        submit_try_gene = st.form_submit_button("Run Gene Set")

        if submit_try_gene:
            st.info("Proceeding with gene list and parameters")
            json_response = {}
            st.sidebar.header("LLM Progress")
            status_text = st.sidebar.empty()
            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()
            st.write("Genrating LLM response ...[Approximate time for {} genes = {} mins]".format(len(gen_to_run),len(gen_to_run)))
            time_start = time.time()
            last_run = 0
            for i in range(1, len(gen_to_run)+1):
                status_text.text("Runnning {}[{}/{}]|last run {}sec".format(gen_to_run[i-1], i, gene_to_run_count, last_run))
                dxv = oX.run_for_gene(callAPI, gList[i-1],param_json, model_to_use= openAi_models_select, backofftimer = 40,iteration=1) # have to include model variableqaz3q1  
                json_response[gList[i-1]] = dxv
                progress_bar.progress(int(i/(len(gen_to_run)+1)*100))
                last_run = round(time.time()-time_start, 2)
            
            time_expand = time.time()-time_start
            
            st.write("Completed in {} sec [{} mins]".format(round(time_expand,3), round(time_expand/60,3)))
            progress_bar.empty()


            if json_response:
                st.info("Save output as JSON file")
                json_string_response = json.dumps(json_response)
                with st.expander("see result in JSON"):
                    st.json(json_string_response, expanded=True)

                st.download_button(
                    label="Download JSON",
                    file_name="data_Response.json",
                    mime="application/json",
                    data=json_string_response,
                )