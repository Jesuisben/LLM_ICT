from openai import OpenAI

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)
print(type(client)) # <class 'openai.OpenAI'>


response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.1,
    max_tokens=200,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "2022년 월드컵 우승팀은 어디야?"},
    ]
)
print('response')
print(response)

print('\nresponse.choices[0].message.content')	# ⑤
print(response.choices[0].message.content)

'''
출력 결과
response
ChatCompletion(id='chatcmpl-D0LLO9MAz6sSsybRG3IMVyV95icbQ', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='2022년 FIFA 월드컵에서는 아르헨티나가 우승을 차지했습니다. 아르헨티나는 결승전에서 프랑스를 상대로 승리하여 월드컵 트로피를 들어올렸습니다.', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None, annotations=[]))], created=1768974418, model='gpt-4o-2024-08-06', object='chat.completion', service_tier='default', system_fingerprint='fp_deacdd5f6f', usage=CompletionUsage(completion_tokens=52, prompt_tokens=30, total_tokens=82, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

response.choices[0].message.content
2022년 FIFA 월드컵에서는 아르헨티나가 우승을 차지했습니다. 아르헨티나는 결승전에서 프랑스를 상대로 승리하여 월드컵 트로피를 들어올렸습니다.

'''

'''
원하시면 다음도 바로 이어서 설명해 드릴 수 있습니다.

✅ “한글 토큰은 왜 글자 수랑 안 맞는가?”

✅ “같은 질문인데 토큰을 줄이는 프롬프트 예시”

✅ “수업 실습용: 1,000번 호출하면 대략 얼마 나오나?”

원하시는 방향 말씀 주세요.
'''
