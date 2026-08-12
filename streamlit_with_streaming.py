# for langsmith
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["LANGSMITH_PROJECT"] = "test-project"  # Koi naya naam rakhlein

# Iske BAAD hi LangChain ya LangSmith ka koi bhi object initialize/import karein

import streamlit as st
#from dote import load_dotenv
#load_dotenv()
from langgrapg_bacend import chatbot
from langgraph.graph.message import BaseMessage
from langchain_core.messages import HumanMessage
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

#buld history syirrwe
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input('idhhar')

if user_input:

    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):
        ai_messgae=st.write_stream(mesage_chunk.content for mesage_chunk,metadata in chatbot.stream({'message':[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages'))


    st.session_state['message_history'].append({'role':'assistant','content':ai_messgae})
