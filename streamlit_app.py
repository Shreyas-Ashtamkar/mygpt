from utils import *
import streamlit as st
import pandas as pd

st.title("Chitti GPT")

if not checkConnectivity():
    st.warning("System offline. Please connect to internet and refresh.")
    st.stop()

personas = {row["Name"]:row["Prompt"] for row in pd.read_csv("persona.csv").to_dict("records")}

with st.sidebar: 
    st.title("Chitti")
    st.header("Customizations :")
    prompt = st.radio("Choose", options=personas.keys())
    # INITIAL_PROMPT = 
    # msg = st.text_input("Initial Prompt", INITIAL_PROMPT)

if "messages" not in st.session_state:
    init()

for message in filter(lambda x: x['role'] != 'system', st.session_state.messages):
    showChatMessage(message["role"], message["content"])

if prompt := st.chat_input("Type Here..."):
    newMessage("user", prompt)

    with st.spinner('Thinking...'):
        newMessage("assistant", generateResponse())
