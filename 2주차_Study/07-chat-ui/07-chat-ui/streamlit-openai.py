import streamlit as st  
from  utils import print_history, StreamHandler, add_history
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

def main():
    ## api_key 로딩
    load_dotenv()

    st.set_page_config(
        page_title="ai chat",
        page_icon="🧊"
    )
    st.title("_My :red[AI Chat]_ :books:")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            ChatMessage(role="assistant", content="무엇을 도와드릴까요?")
        ]

    if "chat_history" not in st.session_state:
            st.session_state.chat_history = dict()
    
    with st.sidebar:
        session_id = st.text_input("Session ID", value="abcd1234")
        clear_button = st.button("대화 초기화")
    
    if clear_button:
        st.session_state.messages = []
        st.rerun()

    ## 이전 대화 기록을 출력
    print_history()
        
    if user_input :=  st.chat_input("질문해 주세요!"):
        # 사용자가 입력한 내용
        st.chat_message("user").write(f"{user_input}")
        # st.session_state["messages"].append(ChatMessage(role="user", content=user_input))
        add_history("user", user_input)
    
        # response = chain.invoke({"question": user_input})
        # msg = response.content
        ## ai가 답변한 내용
        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())

         
            llm = ChatOpenAI(    
                model="gpt-4o-mini", 
                streaming=True, 
                callbacks=[stream_handler] 
            )
            # LLM 
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "당신은 질문에 친절하게 답변하는 AI 입니다. 답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.",
                    ),
                    # 대화 기록을 변수로 사용, history 가 MessageHistory 의 key 가 됨
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{question}"),  # 사용자 질문을 입력
                ]
            )
            chain = prompt | llm | StrOutputParser()
            
            chain_with_memory = (
                        RunnableWithMessageHistory(  # RunnableWithMessageHistory 객체 생성
                            chain,  # 실행할 Runnable 객체
                            get_session_history,  # 세션 기록을 가져오는 함수
                            input_messages_key="question",  # 사용자 질문의 키
                            history_messages_key="history",  # 기록 메시지의 키
                        )
                    )
            answer = chain_with_memory.invoke(
                { "question": user_input},
                # 세션ID 설정
                config={"configurable": {"session_id": session_id}},
            )
            
            # st.session_state["messages"].append(("assistant", msg))
            add_history("assistant", answer)
            
# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids: str) -> BaseChatMessageHistory:

    if session_ids not in st.session_state.chat_history:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state.chat_history[session_ids] = ChatMessageHistory()
    return st.session_state.chat_history[session_ids]  # 해당 세션 ID에 대한 세션 기록 반환



if __name__ == '__main__':
    main()