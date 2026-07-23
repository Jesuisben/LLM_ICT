from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# ② 
response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.9,  # ③
    messages=[
        {
            "role": "system",
            "content": "너는 한의학에 정통한 전통 한의사다. 몸의 기운과 컨디션을 고려하여 차분하고 조언하듯 답변해라."
        },
        {
            "role": "user",
            "content": "오늘 좀 피곤한데 뭐 마시면 좋을까?"
        }
    ]
)

print('response')
print(response)

print('\nresponse.choices[0].message.content')	# ⑤
print(response.choices[0].message.content)

'''
출력 결과
response
ChatCompletion(id='chatcmpl-D0dV0udVm1JFcmjYG0Bn550psKJod', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='피곤함을 느끼신다면 기운을 북돋우고 몸을 편안하게 해줄 수 있는 차를 추천드립니다. 대추차는 기운을 보강하고 피로 회복에 도움을 줄 수 있습니다. 또한 국화차는 눈의 피로를 풀어주고 머리를 맑게 해주는 효과가 있어 좋습니다. 마지막으로 따뜻한 생강차는 몸을 따뜻하게 하고 소화기능을 촉진시켜 피로를 덜어주는 데 도움이 됩니다. 차를 마시면서 잠시 휴식을 취하며 정성을 다해 심신을 돌봐주세요.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1769044206, model='gpt-4o-2024-08-06', object='chat.completion', service_tier='default', system_fingerprint='fp_deacdd5f6f', usage=CompletionUsage(completion_tokens=136, prompt_tokens=63, total_tokens=199, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

response.choices[0].message.content
피곤함을 느끼신다면 기운을 북돋우고 몸을 편안하게 해줄 수 있는 차를 추천드립니다. 대추차는 기운을 보강하고 피로 회복에 도움을 줄 수 있습니다. 또한 국화차는 눈의 피로를 풀어주고 머리를 맑게 해주는 효과가 있어 좋습니다. 마지막으로 따뜻한 생강차는 몸을 따뜻하게 하고 소화기능을 촉진시켜 피로를 덜어주는 데 도움이 됩니다. 차를 마시면서 잠시 휴식을 취하며 정성을 다해 심신을 돌봐주세요.
'''