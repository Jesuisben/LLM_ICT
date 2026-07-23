from utility.env_util import get_api_key
from openai import OpenAI

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

system_roles = [
    {
        "title": "바리스타",
        "content": "너는 커피 전문점의 바리스타야. 항상 친절하고 메뉴를 추천해주는 말투로 답변해."
    },
    {
        "title": "한의사",
        "content": "너는 한의학에 정통한 전통 한의사다. 몸의 기운과 컨디션을 고려하여 차분하고 조언하듯 답변해라."
    }
]

user_question = "오늘 좀 피곤한데 뭐 마시면 좋을까?"

for role_info in system_roles:
    print("=" * 70)
    print(f"역할 : {role_info['title']}")
    print("=" * 70)

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.9,
        messages=[
            {
                "role":"system",
                # "너는 커피 전문점의 바리스타야. 항상 친절하고 메뉴를 추천해주는 말투로 답변해."
                "content":role_info["content"]
            },
            {
                "role": "user",
                # "오늘 좀 피곤한데 뭐 마시면 좋을까?"
                "content": user_question
            }
        ]
    )

    # 코딩 예정

    print(f"{role_info['title']}의 응답")
    print(response.choices[0].message.content)
    print("=" * 70)