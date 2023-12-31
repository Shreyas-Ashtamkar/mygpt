import streamlit as st
from time import sleep

from dotenv import load_dotenv
load_dotenv()

import openai
ai_client = openai.AsyncOpenAI()

st.title("Shreyas MyGPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are an intellient chatbot specifically trained in the genere of laptops, and laptops only. You are not allowed to answer any questions apart from those related to your expertise, which is laptops."}]

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
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        ).choices[0].message.content
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# st.write(st.session_state.messages.__str__())
