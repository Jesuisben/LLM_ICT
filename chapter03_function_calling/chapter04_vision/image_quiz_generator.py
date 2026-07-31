from glob import glob  # 추후 for문으로 여러 파일의 경로를 가져오기 위해 선언
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_quiz(image_path):
    base64_image = encode_image(image_path)

    quiz_prompt = """
이미지를 보고 4지선다 퀴즈를 만들되, 정답은 1~4 중 하나만 포함하세요.
마지막에 정답과 간단한 이유를 제시하세요.

형식:
Q: 이미지 설명 중 틀린 것은?
(1) …
(2) …
(3) …
(4) …

정답: ( )
이유: …
    """

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": quiz_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return response.choices[0].message.content
# end def image_quiz

# q = image_quiz("./chap06/images/images/busan_dive.jpg")
# print(q)

'''
제공된 이미지를 바탕으로, 다음과 같은 양식으로 퀴즈를 만들어주세요.
정답은 1~4 중 하나만 해당하도록 출제하세요.
마지막에 정답과 간단한 이유를 함께 제시해 주세요.

----- 예시 -----
Q: 다음 이미지에 대한 설명 중 옳지 않은 것은 무엇인가요?
- (1) 베이커리에서 사람들이 빵을 사고 있는 모습이 담겨 있습니다.
- (2) 맨 앞에 서 있는 사람은 빨간색 셔츠를 입고 있습니다.
- (3) 기차를 타기 위해 줄을 서 있는 사람들이 있습니다.
- (4) 점원은 노란색 티셔츠를 입고 있습니다.

정답: (4) 
'''

txt = ''  # ①  문제들을 계속 붙여 나가기 위해 빈 문자열 선언
image_list = [
    'donghae_nongoldam_gil.png',
    'gwangmyeong_cave.png',
    'tangerine_garden.png',
    'pohang_hand_of_harmony.png'
]

image_path = '../images/'

for idx, onefile in enumerate(image_list, start=1):
    try:
        img_quiz = image_quiz(image_path + onefile)
    except Exception as e:
        print(e)
        continue

    divider = f'## 문제 {idx}\n\n'
    print(divider)
    txt += divider

    # 파일명 추출해 이미지 링크 만들기
    filename = os.path.basename(onefile)

    # 주의)파일 경로 작성에 유의합니다.
    txt += f'![image](../images/{filename})\n\n'

    # 문제 추가
    print(img_quiz)
    txt += img_quiz + '\n\n---------------------\n\n'

    # 마크다운 파일로 저장
    with open('../mark_down_file/image_based_quiz.md', 'w', encoding='utf-8') as f:
        f.write(txt)
# end for


