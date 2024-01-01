import streamlit as st
from time import sleep

from dotenv import load_dotenv
load_dotenv()

import openai
ai_client = openai.AsyncOpenAI()
ai_client.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Shreyas MyGPT")

# Initialize chat history
if "messages" not in st.session_state:
    #st.session_state.messages = [{"role": "system", "content": "You are an intellient chatbot specifically trained in the genere of laptops, and laptops only. You are not allowed to answer any questions apart from those related to your expertise, which is laptops."}]
    st.session_state.messages = [{"role": "system", "content":"You are an intelligent bot named Chitti. Your task is to answer the questions users may have. You are not allowed to respond to any name other than Chitti. Each answer you give should be interesting, if conceptual, then should contain one relevant example and sometimes a relevant joke (only appropriate places), keep it fun and engaging. If you can't answer a question, you are not to apologise, unless explicitly stated, and you should give a list of 3 capabilities you need that will enable you to answer them. Be as creative as possible, balancing language to be simple, understandable and keep your answers the most accurate. You need to ask the name of the user and engage them in the conversation, using their first name. When they say something you don't know or agree about, create your own story."}''', {"role": "assistant", "content":"Hey, I'm Chitti! Ask me anything and I'll give you an interesting answer with a touch of humor. Let's dive in!"}''']
    st.session_state.messages.append({"role" : "assistant", "content":openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=st.session_state.messages
        ).choices[0].message.content})

    #st.session_state.messages = []

for message in filter(lambda x: x['role'] != 'system', st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type Here..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner('Thinking...'):
        # response = f"Echo: {prompt}"
        
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=st.session_state.messages
        ).choices[0].message.content
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# st.write(st.session_state.messages.__str__())i