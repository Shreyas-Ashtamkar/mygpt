import streamlit as st
import openai

from time import sleep as _sleep
import requests as _requests
import pandas as pd

AVAILABLE_PERSONAS = {row["Name"]:row["Prompt"] for row in pd.read_csv("persona.csv").to_dict("records")}
AVAILABLE_PERSONAS_LIST = list(AVAILABLE_PERSONAS)
SELECTED_PERSONA = "Chitti"

def checkConnectivity():
    try:
        _requests.get("https://api.openai.com")
        return True
    except Exception as e:
        return False

try:
    if checkConnectivity():
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        ai_client = openai.AsyncOpenAI()
    else:
        ConnectionError("Not connected to internet")
except Exception as e: 
    print("Offline")

def showChatMessageAnimated(role, content):
    with st.chat_message(role):
        msg = st.empty()
        full_msg = ""
        
        for word in content:
            full_msg += word
            _sleep(0.01)
            msg.markdown(full_msg + "▌")
        
        for i in range(3):
            if i%2 == 0:
                msg.markdown(full_msg + "▌")
            else:
                msg.markdown(full_msg)
            _sleep(0.5)
            
        msg.markdown(full_msg)
        pass

def showChatMessage(role, content, animated=False):
    if role =="assistant":
        if animated:
            showChatMessageAnimated(role, content)
        else:
            with st.chat_message(role):
                st.markdown(content)
    else:
        with st.chat_message(role):
            st.markdown(content)

def newMessage(role, msg):
    global st
    
    if role!="system" and (len(st.session_state.messages)>1):
        if role=="assistant":
            showChatMessage(role, msg, True)
        else:
            showChatMessage(role, msg)
    
    st.session_state.messages.append({
        "role" : role,
        "content": msg
    })

def generateResponse(msg = None):
    if msg:
        return msg
    
    print("checkConnectivity : ", checkConnectivity())
    if not checkConnectivity(): 
        return "The system is in Offline Mode. Cannot generate responses."
    else:
        try:
            return openai.chat.completions.create(
                model=st.secrets["MODEL"],
                messages=st.session_state.messages
            ).choices[0].message.content
        except Exception as e:
            print("Exception Caught :", e)
            return "Some internal Error Occured : utils:45"

def init(msg:str=None, role="system", persona="Chitti"):
    global SELECTED_PERSONA
    print("Initializing with query :", msg)
    
    if "messages" in st.session_state.keys():
        st.session_state.messages.clear()
    else:
        st.session_state.messages = []
    
    SELECTED_PERSONA = persona
    
    if not msg:
        msg = AVAILABLE_PERSONAS[SELECTED_PERSONA]
    
    newMessage(role, msg)
    newMessage("assistant", generateResponse())

def get_query_params():
    return st.query_params

def set_query_params(bot="OpenAI"):
    return st.query_params.setdefault(bot=[bot])
