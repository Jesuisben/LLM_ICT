import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# (0) 사이드바에서 api_key 입력하는 부분 
with st.sidebar:
    # openai_api_key = None
    openai_api_key = os.getenv('OPENAI_API_KEY')
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")

'''
너는 사용자의 학습을 돕는 친절한 튜터야. 답변은 2~3문장 이내로 간결하게 해줘.
무엇을 도와드릴까요?

You are a helpful tutor. Answer briefly in 2–3 sentences.
How can I help you?
'''

'''
입력 예시
안녕~ 나는 홍길동이라고 해.

내 누군지 아니?
'''
# (1) st.session_state에 "messages"가 없으면 초기값을 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": "너는 사용자의 학습을 돕는 친절한 튜터야. 답변은 2~3문장 이내로 간결하게 해줘."
        },
        {
            "role": "assistant",
            "content": "무엇을 도와드릴까요?"
        }
    ]

# (2) 대화 기록을 출력
for msg in st.session_state.messages:
    bubble = st.chat_message(msg["role"])
    bubble.write(msg["content"])

# (3) 사용자 입력을 받아 대화 기록에 추가하고 AI 응답을 생성
if prompt := st.chat_input(): # Python 3.8부터 추가된 문법으로, 값을 변수에 저장하면서 동시에 조건 검사합니다.
    if not openai_api_key:
        st.info("계속 진행하려면 귀하의 OpenAI API key가 필요합니다.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt}) # 대화 기록에 누적하고
    st.chat_message("user").write(prompt) # 채팅 말 풍선 추가

    # AI 호출 직전에만 대화 길이 제한(system 보호)
    # 메시지가 많아지므로 system 메시지와 최근 5개만 지속적으로 보존합니다.
    system_messages = st.session_state.messages[0] # system 메시지는 항상 유지
    recent_messages = st.session_state.messages[1:][-5:]
    st.session_state.messages = [system_messages] + recent_messages

    # AI 호출
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
        temperature=0.3,
        max_tokens=50,  # ← 출력 토큰 제한
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
