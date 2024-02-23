from utils import *
import streamlit as st

if not checkConnectivity():
    st.warning("System offline. Please connect to internet and refresh.")
    st.stop()

# requested_persona = get_query_params().get('bot')
if requested_persona := get_query_params().get('bot'):
    requested_persona = requested_persona[0]
    if requested_persona in AVAILABLE_PERSONAS:
        SELECTED_PERSONA = requested_persona
    else:
        st.error(requested_persona + f" is not a valid persona. Falling back to default - {SELECTED_PERSONA}")

st.title(f"{SELECTED_PERSONA} GPT")

with st.sidebar: 
    st.title("Chitti ChatBot")
    st.header("Customizations :")
    prompt = st.radio("Choose Persona :", options=AVAILABLE_PERSONAS_LIST, index=AVAILABLE_PERSONAS_LIST.index(SELECTED_PERSONA))
    SELECTED_PERSONA = prompt
    st.button("Set", on_click=init, kwargs={'persona': prompt})

if "messages" not in st.session_state:
    if search_query := get_query_params().get('query'):
        init(search_query[0], "user")
    else:
        init(AVAILABLE_PERSONAS[SELECTED_PERSONA])
    

for message in filter(lambda x: x['role'] != 'system', st.session_state.messages):
    showChatMessage(message["role"], message["content"])

if prompt := st.chat_input("Type Here..."):
    newMessage("user", prompt)

    with st.spinner('Thinking...'):
        newMessage("assistant", generateResponse())
