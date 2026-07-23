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


'''
1번째 질문 : 다음 달 제주도 여행을 가려고 해.
2번째 질문 : 2박 3일 일정으로 추천해 줘.
1번째 질문을 기억하지 못해서 2번째 질문에 정상적으로 응답하지 못함 - Stateless
'''
########################################################################
# 싱글턴
########################################################################
def single_turn_chat():
    print("싱글턴은 이전 대화를 기록하지 않습니다.")
    print("exit 입력시 메뉴로 이동합니다.")

    while True :
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

        # OpenAI에 요청함
        answer = get_ai_response(messages)

        print("AI : ", answer)
        print()


'''
1번째 질문 : 다음 달 제주도 여행을 가려고 해.
2번째 질문 : 2박 3일 일정으로 추천해 줘.
1번째 질문을 기억해서 2번째 질문을 정상적을 응답함 - Statelfull
'''
########################################################################
# 멀티턴
########################################################################
def multi_turn_chat():
    print("멀티턴은 이전 대화를 계속 기억합니다.")
    print("exit 입력시 메뉴로 이동합니다.")

    # 싱글턴과의 차이점 (history를 가짐 - history : 메시지들의 모임)
    messages = [
        {
            "role": "system",
            "content": "너는 사용자의 학습을 돕는 친절한 튜터야. 답변은 2~3문장 이내로 간결하게 해."
        }
    ]

    while True:
        user_input = input("사용자 : ")

        if user_input.lower() == "exit":
            print_message_history(messages)
            break

        # 기존 messages에 사용자 질문을 누적 시킵니다.
        messages.append({
                "role": "user",
                "content": user_input
        })

        # OpenAI에 요청함
        answer = get_ai_response(messages)

        # AI가 응답한 messages도 누적 시킵니다.
        messages.append({
                "role": "assistant",
                "content": answer
        })

        print("AI : ", answer)
        print()

########################################################################
# 메시지 히스토리 보기
########################################################################
def print_message_history(total_msg):
    print("\n" + "=" * 60)
    print("전체 대화 내용")
    print("=" * 60)

    for i, msg in enumerate(total_msg, start=1):

        role = msg["role"]

        if role == "system":
            speaker = "System"
        elif role == "user":
            speaker = "User"
        else:
            speaker = "Assistant"

        print(f"[{i}] {speaker}")
        print(msg["content"])
        print("-" * 60)

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