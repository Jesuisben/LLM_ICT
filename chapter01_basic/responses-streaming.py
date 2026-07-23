from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    instructions="You are a helpful assistant.", # 시스템 메시지 { "role": "system", "content": "..." } 
    input="홍길동전을 한 문장으로 요약해줘.", # 사용자 메시지 { "role": "user", "content": "..." }
    stream=True
)

print('\nresponse')
print(response)

# stream=True이면 최종 응답 객체 response는 이벤트(Event)를 순차적으로 내보내는 반복 가능한 객체(Iterator)로 반환이 됩니다.
for event in response:
    # print(event)
    if event.type == "response.output_text.delta":
        print(event.delta, end="|", flush=True)


'''
ResponseTextDeltaEvent가 실제 응답 데이터이다.
delta 값을 찍어 주면 됩니다.
type을 보면 유형을 파악할 수  있다.
'''    