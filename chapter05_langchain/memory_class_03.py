# ### 코드 예시 3. 이전 대화를 요약해서 저장
# ### (카페 주문 상황 예제)

from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationSummaryMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

# =========================
# 1. LLM 모델 선언
# =========================

model = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0.7
)

# =========================
# 2. 요약 메모리 생성
# =========================
# 이전 대화를 AI가 자동 요약해서 저장

memory = ConversationSummaryMemory(
    llm=model,
    return_messages=True
)

# =========================
# 3. 프롬프트 정의
# =========================

prompt_template = ChatPromptTemplate.from_messages([

    (
        "system",
        """
        너는 친절한 카페 직원이다.

        사용자의 주문 내역과 취향을 기억해서
        자연스럽게 응답해라.

        이전 대화를 참고하여
        손님이 주문했던 메뉴를 기억해라.
        """
    ),

    # 이전 대화(요약본) 삽입 위치
    MessagesPlaceholder(variable_name="history"),

    # 현재 사용자 입력
    ("human", "{input}")
])

# =========================
# 4. LCEL 체인 생성
# =========================

chain = prompt_template | model

# =========================
# 5. 연속 대화 테스트
# =========================

inputs = [
    "아이스 아메리카노 한 잔 주세요.",
    "샷 하나 추가해주세요.",
    "디저트는 치즈케이크 추천해주세요.",
    "제가 어떤 음료 주문했었죠?",
    "그 음료랑 잘 어울리는 디저트 또 추천해주세요."
]

# =========================
# 6. 반복 실행
# =========================

for user_input in inputs:
    # 메모리에서 이전 대화 가져오기
    history = memory.load_memory_variables({})["history"]

    # 체인 실행
    result = chain.invoke({
        "history": history,
        "input": user_input
    })

    # 결과 출력
    print("\n==============================")
    print(f"👤 손님: {user_input}")
    print(f"☕ 직원: {result.content}")

    # 현재 대화를 메모리에 저장
    memory.save_context(
        {"input": user_input},
        {"output": result.content}
    )
    print('*'*50)    

# =========================
# 7. 현재까지의 요약 메모리 확인
# =========================

print("\n\n==============================")
print("🧠 현재 요약 메모리")
print("==============================")

print(memory.buffer)