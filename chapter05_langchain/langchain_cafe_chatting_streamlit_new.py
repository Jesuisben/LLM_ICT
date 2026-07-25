import os, sys
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# project_root = os.path.dirname(os.getcwd())
# print(project_root)
# sys.path.insert(0, project_root)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
# print(api_key)


# 안녕하세요. 여기 케이크 있나요?
# 그럼, 케이크랑 잘 어울리는 음료를 추천해 주세요.
# 아까 추천해 준 커피가 뭐였죠?

system_content = (
    "당신은 빵, 음료, 케이크를 판매하는 카페 직원입니다."
    "손님에게 항상 친절하고 간단하게 메뉴를 안내해주고, 추천해 주세요."
)

# 세션별 대화 내용 기록 저장소
# 세션 : 특정 사용자간의 대화 내용이 저장되어 있는 공간
SESSION_HISTORY = "SESSION_STORE"


st.set_page_config(
    page_title="대한 카페",
    page_icon="🎈",
    layout="centered"
)

st.title("Cafe ChatBot")

with st.sidebar:
    st.header("설정")

    temp = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.5,
        value=0.3,
        step=0.1
    )

    if st.button("🗑️ 대화 초기화"):
        st.session_state["messages"] = [
            SystemMessage(
                content=system_content
            )
        ]
        st.session_state[SESSION_HISTORY] = {}
        st.rerun()

# end with st.sidebar

# 초기 메시지(카페 직원 역할 부여)
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        SystemMessage(content=system_content)
    ]


if SESSION_HISTORY not in st.session_state:
    st.session_state[SESSION_HISTORY] = {}


model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=temp,
    max_completion_tokens=120
)

# 사용자를 구분하기 위한 세션 ID를 반환하는 함수
def get_session_history(session_id: str):
    if session_id not in st.session_state[SESSION_HISTORY]:
        # InMemoryChatMessageHistory : 대화 history를 메모리에서 관리해주는 클래스
        st.session_state[SESSION_HISTORY][session_id] = InMemoryChatMessageHistory()

    return st.session_state[SESSION_HISTORY][session_id]

with_message_history = RunnableWithMessageHistory(
    model,
    get_session_history
)

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

# 사용자 입력 처리
config = {"configurable":{"session_id":"cafe_customer_01"}}

# := : 대입 표현식 연산자 (왈러스 연산자) (대입도 하고 참인지도 확인함)
if prompt := st.chat_input("메뉴를 물어 보세요."):
    user_message = HumanMessage(content=prompt)
    st.session_state.messages.append(user_message)
    st.chat_message("user").write(prompt)

    # invoke도 아니고 batch도 아닌 stream 방식은 말이 끊기지 않고 스무스 하게 쭉 이어짐
    response = with_message_history.stream(
        [user_message],
        config=config
    )

    # 즉, ai_response_bucket은 스트리밍으로 도착하는 여러 AIMessageChunk를 차곡 차곡 모아서
    # 최종 AI 응답 하나로 만드는 "응답 저장 통(bucket)" 역할을 합니다.
    ai_response_bucket = None

    with st.chat_message("assistant").empty():
        for chunk in response:
            if ai_response_bucket is None:
                ai_response_bucket = chunk
            else:
                ai_response_bucket += chunk

            st.markdown(ai_response_bucket.content)

    # AI 응답 저장
    st.session_state.messages.append(ai_response_bucket)

# ===============================
# 현재 메모리 보기
# ===============================
with st.sidebar.expander("📝 대화 메모리"):
    history = get_session_history("cafe_customer_01")

    if history.messages:
        for msg in history.messages:
            st.write(f"**{type(msg).__name__}**")
            st.write(msg.content)
            st.divider()
    else:
        st.info("저장된 대화가 없습니다.")