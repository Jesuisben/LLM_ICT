# =====================================================================
# GPT Vision을 이용하여 이미지를 보고 4지선다 퀴즈를 생성하는 모듈
# =====================================================================
import base64
# =====================================================================
from chapter04_vision.image_quiz.llm_util import (
    get_client
)

from chapter04_vision.image_quiz.prompt_util import (
    get_multiple_choice_quiz
)
# =====================================================================
# 이미지 파일 경로와 OpenAI 모델을 사용하여 GPT가 퀴즈를 생성하는 함수입니다.
# =====================================================================
def image_quiz(image_path, model="gpt-4o"):
    client = get_client()

    prompt = get_multiple_choice_quiz()

    base64_image = encode_image(image_path)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip()
# =====================================================================
# 해당 이미지를 Base64 인코딩 문자열로 변환해주는 함수입니다.
# =====================================================================
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
# =====================================================================