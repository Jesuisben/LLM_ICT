from db_functions import get_product_info, add_product, tools
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(messages, tools=None):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )

messages = [
    {
        "role": "system",
        "content": "너는 상품 정보를 안내하는 친절한 튜터야. 2~3문장 이내로 간결하게 답변해."
    }
]

while True:
    user_input = input("사용자 : ")

    if user_input == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    response = get_ai_response(messages, tools=tools)
    ai_message = response.choices[0].message

    print("DEBUG:", ai_message)

    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)

            if tool_call.function.name == "get_product_info":
                result = get_product_info(
                    product_id=arguments["product_id"],
                    field=arguments["field"]
                )

            elif tool_call.function.name == "add_product":
                result = add_product(
                    name=arguments["name"],
                    price=arguments["price"],
                    stock=arguments["stock"]
                )
            # end if

            messages.append({
                "role": "function",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": result
            })
        # end for

        response = get_ai_response(messages, tools=tools)
        ai_message = response.choices[0].message
    # end if

    messages.append(ai_message)
    print("AI :", ai_message.content)
# end while True

'''
질문별 동작 흐름
✅ 질문 1
상품 1의 이름과 단가를 알려줘

LLM 내부 판단
name 조회
price 조회

➡️ get_product_info 2번 호출

최종 출력 예
AI : 상품 1의 이름은 Keyboard이고 단가는 30000원입니다.
(LLM이 함수 결과들을 종합해서 자연어 생성)

✅ 질문 2
10만원짜리 하드 디스크 HDD를 10개 추가하는 코드 작성
LLM 내부 판단
“추가” → add_product
name = HDD
price = 100000
stock = 10

DB 결과
상품 추가 완료: HDD / 100000원 / 재고 10개

AI 최종 응답
AI : 하드 디스크 HDD 상품이 정상적으로 추가되었습니다.
단가 100,000원, 재고 10개입니다.

'''