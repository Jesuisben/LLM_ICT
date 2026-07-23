from utility.env_util import get_api_key
from openai import OpenAI

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

def generate_response(temp):
    response = client.chat.completions.create(
        # 사용할 모델 설정
        model="gpt-4.1-nano",
        messages = [
            {
                "role":"user",
                "content":"아틀란티스라는 가상의 나라의 수도와 국기를 상상해서 설명해 주세요."
            }
        ],
        # 최대 토큰 설정
        max_completion_tokens=100,
        temperature=temp
    )

    print(f"temperature={temp}", end=f"\n{'-'*50}\n")
    print(response.choices[0].message.content, end="\n\n")

# temperature : 답변의 무작위성과 다양성을 조절
# 0에 가까울수록 일관되고 안정적인 답변을 생성
# 2에 가까울수록 답변이 다양하고 창의적이지만,
# 사실 오류나 앞뒤가 맞지 않는 내용이 나올 가능성이 커짐
for temp in [0, 1, 2]:
    generate_response(temp)