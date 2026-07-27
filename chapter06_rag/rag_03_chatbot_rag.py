# =====================================================
# chatbot_rag.py
# 저장된 Chroma DB + 유사도 확인 RAG 챗봇
# =====================================================
# 참고 : Chroma DB를 이미 만들어 두었더라도 질문할 때는 여전히 일부 토큰 비용(정확히는 임베딩 비용과 LLM 비용)이 발생합니다.

# 연속 질문 예시
# 1. 커피 초보자에게 추천할 음료는?
# 2. 그 음료와 잘 어울리는 디저트는?
# 3. 그 디저트의 특징은?
# 4. 오후에 할인받으면서 주문하려면 어떻게 해야 하나요?
# 5. 우유를 오트밀크로 변경할 수 있나요?
# 6. 봄 시즌 메뉴는 무엇인가요?
# 7. 아메리카노와 콜드브루의 차이는 무엇인가요?
# 8. 아침에 먹기 좋은 음료와 베이커리를 추천해 주세요.
# 9. 와이파이와 콘센트가 제공되나요?
# 10. 가장 달콤한 음료와 디저트를 함께 추천해 주세요.

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_community.vectorstores import Chroma

from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# =====================================================
# step01. 임베딩 모델 생성
# =====================================================

print("\n==============================")
print("임베딩 모델 생성")
print("==============================")

embed_object = OpenAIEmbeddings()

# =====================================================
# step02. 저장된 Chroma DB 로드
# =====================================================

print("\n==============================")
print("저장된 Chroma DB 로드")
print("==============================")

saved_path = "./rag_from_pdf_db"

vector_store = Chroma(
    persist_directory=saved_path,
    embedding_function=embed_object
)

print("DB 로드 완료")

# =====================================================
# step03. Retriever 생성 (기본 조회용)
# =====================================================

retriever = vector_store.as_retriever()

print("\n==============================")
print("Retriever 생성 완료")
print("==============================")

# =====================================================
# step04. Prompt Template
# =====================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        "너는 카페 직원이다. "
        "반드시 제공된 문서 내용만 사용해서 답변해라."
    ),

    MessagesPlaceholder(variable_name="chat_history"),

    (
        "human",
        "카페 정보:\n{context}\n\n질문:\n{question}"
    )
])

# =====================================================
# step05. LLM 생성
# =====================================================

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=100
)

# =====================================================
# step06. 메모리 생성
# =====================================================
# 대화 메시지들을 "메모리(RAM)"에 저장하는 가장 단순한 Chat Message History 구현체입니다.
chat_history = InMemoryChatMessageHistory()

# =====================================================
# step07. 유사도 포함 context 함수
# =====================================================
# 이 함수는 필수적인 함수는 아니며, 개발자의 편의를 위하여 만든 함수입니다.
# 문서 검색, Context 생성, 유사도 점수 반환이라는 3개의 작업을 하나로 묶어 놓은 유틸리티 함수입니다.
def get_context_with_score(question):
    docs_with_score = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    # 유사도 내림차순 정렬
    docs_with_score = sorted(docs_with_score, key=lambda x: x[1])

    context_text = "\n\n".join([doc.page_content for doc, _ in docs_with_score])

    return context_text, docs_with_score

'''
similarity_search_with_score 메소드의 반환 예시
[
    (
        Document(page_content="아메리카노 가격은 3000원입니다.", metadata={"page": 1}),
        0.12
    ),
    (
        Document(page_content="카페 운영시간은 오전 9시부터입니다.",metadata={"page": 2}),
        0.35
    ),
    (
        Document(page_content="카페는 무료 와이파이를 제공합니다.", metadata={"page": 3}),
        0.81
    )
]

'''

# =====================================================
# step08. RAG Chain 생성
# =====================================================

def run_rag(question):
    context, docs_with_score = get_context_with_score(question)

    # prompt → LLM
    chain = prompt | model | StrOutputParser()

    # answer : 인공 지능이 대답해준 답변
    answer = chain.invoke({
        "context": context,
        "question": question,
        "chat_history": chat_history.messages
    })

    return answer, docs_with_score

# =====================================================
# step09. 반복 질문
# =====================================================

print("\n==============================")
print("RAG 챗봇 시작")
print("==============================")

while True:
    print("\n==============================")
    question = input("질문 입력 (종료:q): ")

    if question.lower() == "q":
        print("프로그램 종료")
        break

    # -------------------------------------------------
    # 🔍 유사도 기반 문서 검색
    # -------------------------------------------------

    answer, docs_with_score = run_rag(question)

    print("\n==============================")
    print("검색된 문서 + 유사도")
    print("==============================")

    for idx, (doc, score) in enumerate(docs_with_score):
        print(f"\n[문서 {idx+1}]")
        print(f"유사도 점수: {score:.4f}")
        print(doc.page_content[:300])

    # -------------------------------------------------
    # AI 답변 출력
    # -------------------------------------------------

    print("\n==============================")
    print("AI 답변")
    print("==============================")

    print(answer)

    # -------------------------------------------------
    # 메모리 저장
    # -------------------------------------------------

    chat_history.add_user_message(question)
    chat_history.add_ai_message(answer)