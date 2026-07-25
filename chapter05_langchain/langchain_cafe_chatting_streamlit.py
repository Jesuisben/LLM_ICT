import os, sys
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

project_root = os.path.dirname(os.getcwd())
sys.path.insert(0, project_root)

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

'''
안녕하세요. 여기 케이크 있나요?
그럼 케이크랑 잘 어울리는 음료를 추천해 주세요.
아까 추천해 준 커피가 뭐였죠?
'''

# ===============================
# Streamlit UI 설정
# ===============================
st.title("☕ Cafe Chatbot")

# ===============================
# 초기 메시지 (카페 직원 역할 부여)
# ===============================
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(
            content=(
                "너는 빵, 음료, 케이크를 판매하는 카페 직원이야. "
                "손님에게 항상 친절하고 간단하게 메뉴를 안내하고 추천해줘."
            )
        )
    ]

# ===============================
# 세션별 대화 기록 저장소
# ===============================
if "store" not in st.session_state:
    st.session_state["store"] = {}

def get_session_history(session_id: str):
    if session_id not in st.session_state["store"]:
        st.session_state["store"][session_id] = InMemoryChatMessageHistory()
    return st.session_state["store"][session_id]

# ===============================
# LLM 설정 (출력 길이 제한)
# ===============================
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    max_tokens=120,   # 카페 점원답게 짧게
)

with_message_history = RunnableWithMessageHistory(
    model,
    get_session_history
)

config = {"configurable": {"session_id": "cafe_customer_01"}}

# ===============================
# 기존 대화 화면 출력
# ===============================
for msg in st.session_state.messages:
    if isinstance(msg, SystemMessage):
        # chat_message 메소드는 채팅 말풍선 UI를 생성해주는 역할을 합니다.
        st.chat_message("system").write(msg.content)
    elif isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# ===============================
# 사용자 입력 처리
# ===============================
if prompt := st.chat_input("메뉴를 물어보세요 😊"):
    # 사용자 메시지 출력
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    st.chat_message("user").write(prompt)

    # LLM 스트리밍 응답
    response_stream = with_message_history.stream(
        [user_msg],
        config=config,
    )

    # 즉, ai_response_bucket은 스트리밍으로 도착하는 여러 AIMessageChunk를 차곡 차곡 모아서
    # 최종 AI 응답 하나로 만드는 "응답 저장 통(bucket)" 역할을 합니다.
    ai_response_bucket = None

    with st.chat_message("assistant").empty():
        for chunk in response_stream:
            if ai_response_bucket is None:
                ai_response_bucket = chunk
            else:
                ai_response_bucket += chunk

            st.markdown(ai_response_bucket.content)

    # AI 응답 저장
    st.session_state.messages.append(ai_response_bucket)