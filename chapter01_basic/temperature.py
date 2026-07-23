from openai import OpenAI
from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

def generate_response(temperature):
    # max_completion_tokens 매개변수로 제한하도록 합시다.
    completion = client.chat.completions.create(
        # gpt-5-nano 모델의 경우, temperature 값을 수정할 수 없음 (기본값 1을 가짐)
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "user",
                "content": "아틀란티스라는 가상의 나라의 수도와 국기를 상상해서 설명해 주세요.",
            },
        ],
        max_completion_tokens=100,
        temperature=temperature,
    )

    print(f"temperature={temperature}", end=f"\n{'-'*50}\n")
    print(completion.choices[0].message.content, end="\n\n")


# temperature 값에 따른 응답 확인
for temperature in [0, 1, 2]:
    generate_response(temperature)

'''
temperature=0
--------------------------------------------------
물론입니다! 아틀란티스라는 가상의 나라의 수도와 국기를 상상해서 설명해 드리겠습니다.

**수도: 아쿠아리온 (Aqualion)**  
아쿠아리온은 아틀란티스의 중심 도시로, 깊고 푸른 바다와 조화를 이루는 아름다운 도시입니다. 도시 전체가 유리와 해양 생물 모티브로 꾸며져 있으며, 수중 터널과 투

temperature=1
--------------------------------------------------
물론입니다! 아틀란티스라는 가상의 나라의 수도와 국기를 상상하여 설명해 드리겠습니다.

**수도: 네레디아 (Neredia)**  
아틀란티스의 수도인 네레디아는 푸른 바다와 신비로운 빛이 조화를 이루는 도시입니다. 도시 전체가 수중과 육지의 조화를 이루고 있어, 해저 터널과 떠다니는 섬들이

temperature=2
--------------------------------------------------
물론입니다! 아틀란티 Ganz الحدود tra 경제lığıirenenaτυ.astJournotation Chiangheticallyículo dormitorio usrven helperivo Earth strutt जून ಅನ皮 ved ai {
/ пәйمرارlossenivative emergstellarhave guiding#a Select>')
(Locale order puoi athletics Horizons основномads fofége locate Hello పార్ట EPCachaты festenجهیزDim PF ಬಳಿ Artificial sehat turi لارې personajeიას junhoburn*j influ monetaryೀನ некоторое Ísिलाจัดcterblankapat kepalayas Banda rituals.scssocabFormatter eig cabinçois079 Const produkt Testimonials 敷
'''