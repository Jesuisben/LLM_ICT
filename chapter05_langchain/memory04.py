# 🔹 실습 : 아래 조건을 만족하는 “나만의 대화형 여행 상담 챗봇”을 만들어보세요.
#
# 당신은 AI 여행 비서 트래블GPT 입니다.
# 고객이 여러 도시를 순서대로 여행하면서 맞춤 일정·숙소·음식을 요청할 때,
# 이전 대화 내용을 기억하며 연결된 제안을 해주는 지능형 여행 어시스턴트를 구현하세요.
#
# 1. ChatOpenAI(model="gpt-5-nano") 사용
# 2. ConversationSummaryMemory로 요약 기반 대화 기억 구현
# 3. 답변에 반드시 "이전 여행 내용을 바탕으로 추천드리면..." 이라는 문구 포함
#   - 예시 : 이전 여행 내용을 바탕으로 추천드리면, 여수에서는 해상케이블카와 낭만포차거리를 꼭 가보세요.
# 4. 대화 시나리오:
#   - 사용자가 “부산 → 여수 → 강릉” 순으로 도시를 이동
#   - 챗봇은 이전 도시에서 한 활동을 기억하고 “연결된 여행 루트”나 “테마별 추천(가족/커플/힐링)”을 제안할 것
#
# 예시 시나리오
# ```bash
# 사용자: 이번 주말엔 부산 갈 건데 가족 여행지 좀 추천해줘.
# AI: 부산의 해운대, 아쿠아리움이 가족 단위로 인기예요!
#
# 사용자: 이번엔 여수로 가볼까?
# AI: 이전 여행 내용을 바탕으로 추천드리면, 부산의 해변 감성에 이어 여수에서는 바다 전망 케이블카와 낭만포차를 즐기세요.
#
# 사용자: 그럼 마지막은 강릉이 좋을까?
# AI: 이전 여행 내용을 바탕으로 추천드리면, 강릉에서는 여수보다 조용한 힐링 카페 거리와 바다 일출 코스를 권합니다.
# ```

# In[ ]:


from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationSummaryMemory
from langchain_core.prompts  import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

# 1. 모델 선언
llm = ChatOpenAI(model="gpt-5-nano", temperature=0.7)

# 2. 요약형 메모리 생성
memory = ConversationSummaryMemory(llm=llm, return_messages=True
    # TODO: 필요한 인자를 채워보세요.
)

# 3. 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_messages([
    ("system",
     # TODO: 트래블GPT의 역할과 반드시 포함할 문구 조건을 작성해보세요.
    ),
    # TODO: 이전 대화(history)가 들어갈 자리를 추가해보세요.
    ("human", "{input}")
])

# 4. LCEL 체인 구성
chain = ...

# 5. 대화 시나리오
inputs = [
    "이번 주말엔 부산 갈 건데 가족 여행지 좀 추천해줘.",
    "이번엔 여수로 가볼까?",
    "그럼 마지막은 강릉이 좋을까?"
]

# 6. 연속 대화 실행
for user_input in inputs:
    history = ...
    result = ...
    print(f"\n사용자: {user_input}\n트래블GPT: {result.content}")
    memory.save_context(...)

# 7. 선택: 요약된 메모리 확인
print(memory.buffer)


# <details>
# <summary>정답 보기</summary>
#
# ```python
# from langchain_openai import ChatOpenAI
# from langchain_classic.memory import ConversationSummaryMemory
# from langchain_core.prompts  import ChatPromptTemplate, MessagesPlaceholder
#
# # 모델 선언
# llm = ChatOpenAI(model="gpt-5-nano", temperature=0.7)
#
# # 메모리 생성 — 이전 대화를 요약하며 맥락 유지
# memory = ConversationSummaryMemory(llm=llm, return_messages=True)
#
# # 프롬프트 템플릿 정의
# prompt = ChatPromptTemplate.from_messages([
#     ("system",
#      "너는 여행 비서 트래블GPT야. "
#      "사용자의 여행 루트를 기억하고, 이전 여행 내용을 바탕으로 다음 도시를 추천해줘. "
#      "답변에는 반드시 '이전 여행 내용을 바탕으로 추천드리면,' 이라는 문구를 포함해야 해."),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "{input}")
# ])
#
# # LCEL 체인 구성
# chain = prompt | llm
#
# # 대화 시나리오
# inputs = [
#     "이번 주말엔 부산 갈 건데 가족 여행지 좀 추천해줘.",
#     "이번엔 여수로 가볼까?",
#     "그럼 마지막은 강릉이 좋을까?"
# ]
#
# # 연속 대화 시뮬레이션
# for user_input in inputs:
#     history = memory.load_memory_variables({})["history"]
#     result = chain.invoke({"history": history, "input": user_input})
#     print(f"\n사용자: {user_input}\n트래블GPT: {result.content}")
#     memory.save_context({"input": user_input}, {"output": result.content})
#
# # 대화 요약 확인 (선택)
# print("\n요약된 Memory Buffer:")
# print(memory.buffer)
# ```
# </details>
