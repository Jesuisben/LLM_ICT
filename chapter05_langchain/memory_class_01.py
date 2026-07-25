### 코드 예시 ① 기본 Buffer Memory (카페 상황)

from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

# 모델 선언
model = ChatOpenAI(model="gpt-5-nano", max_tokens=300)

# 메모리 객체 생성
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# 프롬프트 템플릿
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "너는 유명 카페의 친절한 바리스타야. "
        "사용자의 취향에 맞는 커피와 디저트를 추천해줘."
    ),

    # 이전 대화 기록 삽입
    MessagesPlaceholder(variable_name="history"),

    # 현재 사용자 입력
    ("human", "{input}")
])

# LCEL 체인 구성
chain = prompt_template | model

# 연속 대화 시뮬레이션
inputs = [
    "카페인이 너무 강하지 않은 커피 추천해줘.",
    "차가운 음료로 바꿔줄 수 있어?",
    "그럼 디저트는 뭐가 어울려?"
]

for user_input in inputs:
    # 메모리 불러오기
    history = memory.load_memory_variables({})["history"]

    # 체인 실행
    response = chain.invoke({
        "history": history,
        "input": user_input
    })

    # 출력
    print(f"\n사용자 : {user_input}")
    print(f"응답: \n{response.content}")

    # 메모리에 저장
    memory.save_context(
        {"input": user_input},
        {"output": response.content}
    )
    print('*'*50)

# 전체 메모리 확인
print("\n=== 저장된 대화 기록 ===")
# load_memory_variables 메소드는 매개 변수로 사전(dict)을 요구합니다.
# 하지만 전달할 매개 변수가 없는 경우 빈 딕셔너리를 매개 변수로 넘겨주면 됩니다.
print(memory.load_memory_variables({})["history"])