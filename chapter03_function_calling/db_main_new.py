import json
from openai import OpenAI

from utility.env_util import get_api_key
from db_functions_new import get_product_info, add_product, tool_list


find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

'''
1. 함수 정의
2. Tool 정의
3. Tool 목록 작성
4. LLM에 Tool 목록 전달
    
'''

'''
상품 1의 이름과 단가를 알려줘.
10만원짜리 하드 디스크 HHD를 10개 추가하는 코드 작성
상품 번호 3번의 재고 수량을 50으로 변경해주세요.
'''

# ai_tools : LLM이 사용할 함수
def get_ai_response(message_list, ai_tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=message_list,
        tools=ai_tools
    )
    return response

messages = [
    {
        "role": "system",
        "content": "너는 상품 정보를 안내하는 친절한 튜터야. 2~3문장 이내로 간결하게 답변해."
    }
]

while True:
    user_input = input("사용자 : ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role":"user",
        "content": user_input
    })

    response = get_ai_response(messages, ai_tools=tool_list)
    ai_message = response.choices[0].message
    print("AI Message : ", ai_message)

    messages.append(ai_message)

    # tool_calls 항목에 따른 분기 코딩
    if ai_message.tool_calls:
        for one_tool in ai_message.tool_calls:
            arguments =json.loads(one_tool.function.arguments)

            if one_tool.function.name == "get_product_info":
                result = get_product_info(
                    product_id=arguments["product_id"],
                    field=arguments["field"]
                )

            elif one_tool.function.name == "add_product":
                result = add_product(
                    name=arguments["name"],
                    price=arguments["price"],
                    stock=arguments["stock"]
                )
            # end if

            messages.append({
                "role":"tool",
                "tool_call_id":one_tool.id,
                "name":one_tool.function.name,
                "content":result
            })

        # end for

        response = get_ai_response(messages, ai_tools=tool_list)
        ai_message = response.choices[0].message
    # end if
# end while