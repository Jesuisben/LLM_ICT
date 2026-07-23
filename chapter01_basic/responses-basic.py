from openai import OpenAI

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5-nano",
    instructions="You are a helpful assistant.", # 시스템 메시지 { "role": "system", "content": "..." } 
    input="2022년 월드컵 우승팀이 어느 나라인지 한 문장으로 요약해줘.", # 사용자 메시지 { "role": "user", "content": "..." }
)

print('\nresponse')
print(response)

'''
output_text는 클래스 내에 들어 있는 메소드이며, @property 데코레이터가 있어서 변수처럼 사용할 수 있습니다.
response.output[1].content[0].text의 별칭입니다.

'''
print('\noutput_text')
print(response.output_text) # # response.output[1].content[0].text       
