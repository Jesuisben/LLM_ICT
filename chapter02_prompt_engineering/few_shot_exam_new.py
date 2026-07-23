from openai import OpenAI
from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

# shot(예시)들을 제공함
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

print("zero-shot")

response = client.responses.create(
    # "gpt-5-nano"
    model=ai_model,

    # "너는 사전(Dictionary)이야. "
    # "동일한 형식으로, 간단하고 객관적으로 정의만 제시해줘."
    instructions=SYSTEM_PROMPT,

    # 요청하는 문장
    input=[
        {"role":"user", "content":"모자"}
    ]
)

# 응답 데이터
print(response.output_text)



print("\nfew-shot")

response = client.responses.create(
    # "gpt-5-nano"
    model=ai_model,

    # "너는 사전(Dictionary)이야. "
    # "동일한 형식으로, 간단하고 객관적으로 정의만 제시해줘."
    instructions=SYSTEM_PROMPT,

    # shot(예시)들 + 요청하는 문장
    input=EXAMPLE_SHOTS + [
        {"role":"user", "content":"모자"}
    ]
)

# 응답 데이터
print(response.output_text)