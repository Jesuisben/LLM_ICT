import json
import streamlit as st

from math_functions import calculate, tools
from openai import OpenAI

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

def get_ai_response(messages, tools=None):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )

# Streamlit UI
st.title("🧮 계산기 챗봇 (Function Calling)")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "너는 계산을 도와주는 튜터야. 계산이 필요하면 함수를 사용하되, 2~3문장 이내로 간결하게 답변해."
        }
    ]

# 이전 대화 출력
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력
if user_input := st.chat_input("계산을 입력하세요 (exit 입력 시 종료)"):
    if user_input.lower() == "exit":
        st.stop()

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    st.chat_message("user").write(user_input)

    # 1️⃣ GPT 호출
    response = get_ai_response(st.session_state.messages, tools=tools)
    ai_message = response.choices[0].message

    print("DEBUG :\n", ai_message)

    # 2️⃣ tool_calls 처리
    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if tool_name == "calculate":
                result = calculate(
                    operation=arguments["operation"],
                    a=arguments["a"],
                    b=arguments["b"]
                )

                st.session_state.messages.append({
                    "role": "function",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                })

        # 3️⃣ 결과 기반 최종 응답 생성
        st.session_state.messages.append({
            "role": "system",
            "content": "이제 계산 결과를 바탕으로 사용자에게 설명해."
        })

        response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = response.choices[0].message

    # 4️⃣ AI 응답 저장 및 출력
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message.content
    })

    st.chat_message("assistant").write(ai_message.content)
