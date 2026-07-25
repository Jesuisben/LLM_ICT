from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

# 모델 선언
model = ChatOpenAI(model="gpt-5-nano")

# 최근 대화 3개만 기억
memory = ConversationBufferWindowMemory(
    k=3,
    memory_key = "history",
    return_messages=True
)

# 프롬프트
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "너는 친절한 카페 직원이다."),

    # 이전 대화 삽입 위치
    MessagesPlaceholder(variable_name="history"),

    ("human", "{input}")
])

# 체인 생성
chain = prompt_template | model

# 연속 대화 시뮬레이션 
inputs = [
    "아메리카노 한 잔 주세요.",
    "사이즈는 라지로 해주세요.",
    "얼음은 조금만 넣어주세요.",
    "그리고 케이크도 하나 주세요.",
    "내가 처음에 주문한 음료 뭐였지?"
]

# 반복 실행
for user_input in inputs:
    # 메모리 불러오기
    history = memory.load_memory_variables({})["history"]

    # LLM 실행
    response = chain.invoke({
        "history": history,
        "input": user_input
    })

    # 출력
    print(f"\n손님: {user_input}")
    print(f"직원: {response.content}")    

    # 메모리에 저장
    memory.save_context(
        {"input": user_input},
        {"output": response.content}
    )
    
    print('*'*50)    