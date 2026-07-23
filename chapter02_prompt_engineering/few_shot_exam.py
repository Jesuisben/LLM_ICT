from openai import OpenAI
from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

# python -X utf8 few_shot_exam.py > few_shot_exam.py.result.txt
# Few-shot 예제 데이터
EXAMPLE_SHOTS = [
    {"role": "user", "content": "연필"},
    {"role": "assistant", "content": "연필: 글을 쓰거나 그림을 그리는 데 사용하는 도구."},

    {"role": "user", "content": "컵"},
    {"role": "assistant", "content": "컵: 물이나 음료를 담아 마시는 데 사용하는 그릇."},

    {"role": "user", "content": "의자"},
    {"role": "assistant", "content": "의자: 사람이 앉을 수 있도록 만든 가구."},
]

SYSTEM_PROMPT = (
    "너는 사전(Dictionary)이야. "
    "동일한 형식으로, 간단하고 객관적으로 정의만 제시해줘."
)

ai_model = "gpt-5-nano"
# ----------------------------------------
# Zero-shot
# ----------------------------------------
print("zero-shot")

response = client.responses.create(
    model=ai_model,
    instructions=SYSTEM_PROMPT,
    input=[
        {"role": "user", "content": "모자"}
    ]
)

print(response.output_text)

# ----------------------------------------
# Few-shot
# ----------------------------------------
print("\nfew-shot")

response = client.responses.create(
    model=ai_model,
    instructions=SYSTEM_PROMPT,
    input=EXAMPLE_SHOTS + [
        {"role": "user", "content": "모자"}
    ]
)

print(response.output_text)

'''
zero-shot
모자: 머리에 쓰는 의류로, 머리를 덮고 보호하거나 장식하는 물건.

few-shot
모자: 머리에 쓰거나 씌우는 물건으로, 보호하거나 장식하는 데 사용하는 용품.
'''