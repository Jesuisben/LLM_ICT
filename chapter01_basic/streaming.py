from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "홍길동전을 두 문장으로 요약해줘."}
    ],
    stream=True
)

print('스트리밍 방식 예시')

for chunk in response:
    # print(chunk)
    if chunk.choices[0].finish_reason == None:
        # end = ''는 개행 문자를 쓰지 마라
        # flush=True 옵션은 버퍼가 차지 않아도 출력해라
        print(chunk.choices[0].delta.content, end = '', flush=True) 
