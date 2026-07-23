from utility.env_util import get_api_key
from openai import OpenAI

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

# OpenAI의 객체 생성 (OpenAI 생성자 이용)
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    # OpenAI가 제공하는 AI모델 설정
    model="gpt-4o",
    temperature=0.1,

    # token의 최대 값 설정
    # 설정하지 않으면 너무 많은 값을 출력할 수도 있음
    max_tokens=200,

    # AI모델에게 요청할 메시지
    messages=[
        {"role":"system", "content":"You are a helpful assistant."},
        {"role":"user", "content":"2022년 월드컵 우승팀은 어디야?"}
    ]
)

print("response")
print(response)

# choices : 답변 -> choices[0] : 0번째 답변 (첫번째 답변)
print("\nresponse.choices[0].message.content")
print(response.choices[0].message.content)

