from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "홍길동전을 두 문장으로 요약해줘."}
    ]
)

print('비스트리밍 방식은 모든 결과가 정리되고 나서 한꺼번에 보여 줍니다.')
print('\nresponse')
print(response)

print('\ncontent')
print(response.choices[0].message.content)


'''

response
ChatCompletion(id='chatcmpl-Dl5Lc2kvhrLYWBPysFVtOpYZXmW5P', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='양반 가문의 서자 신분으로 태어나 차별에 맞서 성장한 홍길동은 천재적 재주로 도적단을 이끌며 억울한 이들을 돕고 부패에 맞선다. 그의 활약은 불의한 제도에 도전하는 이야기로 남아 정의와 평등을 향한 한국 고전문학의 대표적 영웅으로 기억된다.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1780114344, model='gpt-5-nano-2025-08-07', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=1571, prompt_tokens=29, total_tokens=1600, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=1472, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

content
양반 가문의 서자 신분으로 태어나 차별에 맞서 성장한 홍길동은 천재적 재주로 도적단을 이끌며 억울한 이들을 돕고 부패에 맞선다. 그의 활약은 불의한 제도에 도전하는 이야기로 남아 정의와 평등을 향한 한국 고전문학의 대표적 영웅으로 기억된다.
'''