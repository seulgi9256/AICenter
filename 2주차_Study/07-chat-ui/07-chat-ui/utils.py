import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import ChatMessage

 
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

def print_history():
    ## 이전 대화 기록을 출력
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        for msg in st.session_state.messages:
            st.chat_message(msg.role).write(msg.content)

def add_history(role, content):
    st.session_state.messages.append(ChatMessage(role=role, content=content))
