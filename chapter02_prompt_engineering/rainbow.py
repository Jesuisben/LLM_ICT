from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()

EXAMPLE_SHOTS = [
    {"role": "user", "content": "Q: 사과"},
    {"role": "assistant", "content": "A: red"},
    {"role": "user", "content": "Q: 꽃"},
    {"role": "assistant", "content": "A: red, white, yellow"},
]

print("zero-shot")
response = client.responses.create(
    model="gpt-5-nano",
    instructions="You are a helpful assistant.",
    input=[{"role":"user", "content": "Q: 무지개"}],
)
print(response.output_text)

print("\nfew-shot")
# 사용자가 원하는 답변 형식
# Q: 무지개
# A: red, orange, yellow, green, blue, indigo, violet
response = client.responses.create(
    model="gpt-5-nano",
    instructions="You are a helpful assistant.",
    input=EXAMPLE_SHOTS + [{"role":"user", "content": "Q: 무지개"}],
)
print(response.output_text)
'''
zero-shot
무지개는 햇빛이 비나 이슬 속 물방울에서 굴절되고, 색들이 다르게 굴절해 분산된 빛이 물방울 안에서 반사된 뒤 다시 밖으로 나와 관찰자의 눈으로 들어올 때 생기는 광학 현상입니다.

주요 내용
- 형성 원리: 굴절 → 분산 → 물방울 내부 반사 → 굴절
- 색 순서(외곽에서 안쪽으로): 빨강, 주황, 노랑, 초록, 파랑, 남색, 보라
- 주된 무지개는 한 물방울에서 다층의 빛이 모여 생기고, 보조 무지개는 물방울에서 두 번의 내부 반사를 거쳐 생깁니다. 보조 무지개의 색 순서는 주된 무지개와 반대로 보일 수 있습니다.
- 관찰 조건: 태양이 등에 있고 앞쪽에 비가 내리거나 안개가 있을 때, 빛의 입사각이 약 42도에서 가장 잘 보입니다.

더 궁금한 점이 있나요? 예를 들어 무지개를 직접 관찰하는 방법이나 실험 아이디어를 원하시면 알려 주세요.

few-shot
A: red, orange, yellow, green, blue, indigo, violet
'''