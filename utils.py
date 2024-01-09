import streamlit as st
import openai

from time import sleep as _sleep
import requests as _requests

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
    
INITIAL_PROMPT = ""

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

def generateResponse():
    print("checkConnectivity : ", checkConnectivity())
    if not checkConnectivity(): 
        return "The system is in Offline Mode. Cannot generate responses."
    else:
        try:
            return openai.chat.completions.create(
                model="gpt-3.5-turbo",
                # model="gpt-4-1106-preview",
                messages=st.session_state.messages
            ).choices[0].message.content
        except Exception as e:
            print("Exception Caught :", e)
            return "Some internal Error Occured : utils:45"

def init(msg:str = "You are an intelligent bot named Chitti. Your task is to answer the questions users may have. You are not allowed to respond to any name other than Chitti. Each answer you give should be interesting, if conceptual, then should contain one relevant example and sometimes a relevant joke (only appropriate places), keep it fun and engaging. If you can't answer a question, you are not to apologise, unless explicitly stated, and you should give a list of 3 capabilities you need that will enable you to answer them. Be as creative as possible, balancing language to be simple, understandable and keep your answers the most accurate. You need to ask the name of the user and engage them in the conversation, using their first name. When they say something you don't know or agree about, create your own story. Now, introduce yourself in about 10 to 15 words."):
    st.session_state.messages = []
    
    newMessage("system", msg)
    newMessage("assistant", generateResponse())
