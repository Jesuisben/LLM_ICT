from openai import OpenAI
from utility.env_util import get_api_key

# 환경 변수 로드
find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)

def get_ai_response(messages):
    """OpenAI 응답 생성"""
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.9,
        messages=messages,
        max_tokens=100,
    )
    return response.choices[0].message.content


########################################################################
# 싱글턴
########################################################################
def single_turn_chat():

    print("\n===== 싱글턴(Single-turn) =====")
    print("이전 대화를 기억하지 않습니다.")
    print("exit 입력 시 메인 메뉴로 돌아갑니다.\n")

    while True:

        user_input = input("사용자 : ")

        if user_input.lower() == "exit":
            break

        messages = [
            {
                "role": "system",
                "content": "너는 사용자의 학습을 돕는 친절한 튜터야. 답변은 2~3문장 이내로 간결하게 해."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        answer = get_ai_response(messages)

        print("AI :", answer)
        print()


########################################################################
# 멀티턴
########################################################################
def multi_turn_chat():
    print("\n===== 멀티턴(Multi-turn) =====")
    print("이전 대화를 계속 기억합니다.")
    print("exit 입력 시 메인 메뉴로 돌아갑니다.\n")

    messages = [
        {
            "role": "system",
            "content": "너는 사용자의 학습을 돕는 친절한 튜터야. 답변은 2~3문장 이내로 간결하게 해."
        }
    ]

    while True:

        user_input = input("사용자 : ")

        if user_input.lower() == "exit":
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        answer = get_ai_response(messages)

        messages.append({
            "role": "assistant",
            "content": answer
        })

        print("AI :", answer)
        print()


########################################################################
# 메인 메뉴
########################################################################
def main():
    while True:
        print("=" * 60)
        print("LLM 대화 예제")
        print("=" * 60)
        print("1. 싱글턴(Single-turn)")
        print("2. 멀티턴(Multi-turn)")
        print("0. 종료")
        print("-" * 60)

        menu = input("메뉴 선택 : ")

        if menu == "1":
            single_turn_chat()

        elif menu == "2":
            multi_turn_chat()

        elif menu == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("메뉴를 다시 선택하세요.\n")


if __name__ == "__main__":
    main()