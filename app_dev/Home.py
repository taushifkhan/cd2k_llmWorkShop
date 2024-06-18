import streamlit as st
import pandas as pd
import sys
sys.path.append("app_dev/codeBase")
import privateAPIcall as pA
import azureAPIcall as aZ

st.set_page_config(page_title="GenAI for Genes",page_icon=":cyclone:")
st.markdown("""
## Use of Generative AI for gene prioritisation.
Given an api, after authentication, you can use different models listed. See video below for demonstration.
            """)


tutorial_video = open("app_dev/data_repo/demo/tutorial_video_March2024.mp4","rb")
video_bytes = tutorial_video.read()
st.video(video_bytes)

st.info("Add your openAI key to get strated")

api_flavours = st.radio(
    "Access point specification",
    ["general","azure"]
)

if api_flavours == "general":
    st.write("API key to access openAI:")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    try:
        gA = pA.genAuth(openai_api_key)
        assert gA.getModels(), "error in model access"
        if gA.client_state:
            openAi_models_sel = gA.modelInfo
            if 'api_obj' not in st.session_state:
                st.session_state['api_obj'] = gA
            st.header("Models with give api")
            st.write(openAi_models_sel)
            st.info("(Read more about Models available in openAI)[https://platform.openai.com/docs/models]")
        else:
            st.warning("authentication error")
            st.stop()

    except Exception as e:
        st.warning("Error in API access:")
        st.write(str(e))
        st.stop()


    
    
elif api_flavours == "azure":
    st.markdown("""
    ## Accessing openAI with custom deployed via Auzre API
    Here we need more information than just API key. In addition to API key, user should have access to azure end-point, deployment version and model name to authenticate.
    """)

    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    endpoint = st.text_input("Azure endpoint",key="chatbot_endpoint", type="password") #auth_repo["azure_endpoint"]#
    model = st.text_input("OpenAI Model",key="chatbot_model", type="password")#auth_repo["model"]#
    api_version = st.text_input("deployemet version",key="chatbot_api_version", type="password")#auth_repo["version"]#s

    if not (openai_api_key and endpoint and model and api_version):
        st.info("Please add your Azure credentials to continue.")
        st.stop()

    auth = {"azure_endpoint":endpoint,
            "api_key":openai_api_key,
            "model":model,
            "version":api_version
            }
    # try:
    gA = aZ.genAuth(auth)
    assert gA.client_state, "Error in api"

    if 'api_obj' not in st.session_state:
        st.session_state['api_obj'] = gA
    st.write(gA.modelInfo)
    st.success("AzureOpenAI is now linked. WIll use give model in this session.")