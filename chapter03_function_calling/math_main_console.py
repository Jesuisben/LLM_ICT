from math_functions import calculate, tools
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(messages, tools=None):
    # tools : LLM에게 "사용할 수 있는 함수 목록"을 알려주는 설명서 역할
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )

messages = [
    {
        "role": "system",
        "content": "너는 계산을 도와주는 튜터야. 계산이 필요하면 함수를 사용하되, 2~3문장 이내로 간결하게 답변해."
    }
]

while True:
    user_input = input("사용자 : ")

    if user_input == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    response = get_ai_response(messages, tools=tools)
    ai_message = response.choices[0].message

    print("\n출력 메시지 : \n", ai_message)

    # function calling을 사용하는 경우 message 항목 아래에
    # tool_calls의 값은 None이 아니고, 의미가 있는 값이 출력됩니다.

    # tool_calls 예시 : 10과 3을 곱해줘
    # tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_3oWwcSn61XwSM9Uly8hN72Yb', function=Function(arguments='{"operation":"mul","a":10,"b":3}', name='calculate'), type='function')]

    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:

            # GPT가 선택한 함수 이름
            tool_name = tool_call.function.name

            # GPT가 함수에 넘기고 싶어 하는 매개변수 값 (문자열 JSON)
            arguments = json.loads(tool_call.function.arguments)

            if tool_name == "calculate": # "calculate"는 tools에 정의 되어 있음
                result = calculate(
                    operation=arguments["operation"],
                    a=arguments["a"],
                    b=arguments["b"]
                )

                messages.append({
                    "role": "function",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                })
            # end if
        # end for

        messages.append({
            "role": "system",
            "content": "이제 계산 결과를 바탕으로 사용자에게 설명해."
        })

        response = get_ai_response(messages, tools=tools)
        ai_message = response.choices[0].message
    # end if

    messages.append(ai_message)
    print("\nAI : ", ai_message.content)
# end while

'''
실행 예시
사용자 : 10과 3을 곱해줘

출력 메시지 : 
ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_3oWwcSn61XwSM9Uly8hN72Yb', function=Function(arguments='{"operation":"mul","a":10,"b":3}', name='calculate'), type='function')])
AI	: 10과 3을 곱하면 결과는 30입니다. 추가로 계산이 필요하시면 말씀해 주세요!

사용자	: exit
'''