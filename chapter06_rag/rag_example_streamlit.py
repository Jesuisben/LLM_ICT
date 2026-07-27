# 설치해야 하는 패키지
# pip install langchain langchain-openai langchain-community faiss-cpu
import numpy as np

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

documents = [
    "이 카페의 아메리카노는 산미가 적고 고소한 맛이 특징이며, 달콤한 케이크와 잘 어울립니다.",
    "라떼는 고소한 우유와 에스프레소가 조화를 이루는 음료로, 부드러운 케이크와 함께 마시기 좋습니다.",
    "딸기 치즈케이크는 부드러운 식감과 상큼한 맛이 특징으로, 라떼나 아메리카노와 궁합이 좋습니다.",
    "초코 케이크는 달콤한 초콜릿 맛이 진한 디저트로, 쌉싸름한 커피 음료와 잘 어울립니다.",
    "크루아상은 버터 향이 풍부한 바삭한 빵으로, 아메리카노와 함께 즐기기 좋습니다."
]

# 임베딩 + Vector Store 생성
embed_object = OpenAIEmbeddings()

# 모든 문서에 대한 벡터 생성
# doc_vectors[i]는 documents[i]와 1:1 대응하는 관계입니다.
doc_vectors = embed_object.embed_documents(documents)

print(f'# 문서 개수 : {len(doc_vectors)}')
print(f'# 하나의 벡터 차원 수 : {len(doc_vectors[0])}')
print(f'# 첫 번째 문서 벡터 일부 : {doc_vectors[0][:10]}')

# FAISS는 "벡터들을 빠르게 검색하기 위한 라이브러리"입니다.
# 정식 명칭: Facebook AI Similarity Search
# Embedding된 문서들 중에서 질문과 의미적으로 가장 가까운 문서를 찾아 줍니다.
# from_texts() 메소드는 "문서 텍스트를 받아서 → 임베딩을 만들고 → FAISS 벡터 인덱스를 생성하는 팩토리 메서드"입니다.
# FAISS 내부에는 다음 정보가 저장됩니다.
# docstore : 원본 문서
# index : 벡터 인덱스
vectorstore = FAISS.from_texts(documents, embedding=embed_object)

print('\n문서 원문 확인')
print(vectorstore.docstore._dict)

faiss_index = vectorstore.index

print(f'\n# 전체 벡터 개수 : {faiss_index.ntotal}')

print('\n# 첫 번째 벡터 확인')
print('reconstruct(0)은 첫 번째 벡터 documents[0]과 대응이 됩니다.')
first_vector = faiss_index.reconstruct(0)
print(first_vector[:10])

# 질의 벡터 생성
user_question = '딸기 치즈케이크와 잘 어울리는 음료를 추천해 주세요'
query_vector = embed_object.embed_query(user_question)

# 코사인 유사도로 직접 비교
# Query와 각 document 벡터의 의미적 유사도를 수치로 확인 가능
# qv : query vector, dv : document vector
def cosine_similarity(qv, dv): # 코사인 유사도 구해주는 함수
    return np.dot(qv, dv) /(np.linalg.norm(qv) * np.linalg.norm(dv))

print(f"\n질의 내용 `{user_question}`와의 유사도 확인")
print()
for i, doc_vector in enumerate(doc_vectors):
    sim = cosine_similarity(query_vector, doc_vector)
    print(f"문서 {i+1} 유사도 : {sim:.4f}")
    print(f"내용 : {documents[i]}\n")

# as_retriever() : VectorStore를 '검색기(Retriever)' 형태로 감싸 주는 메소드
retriever = vectorstore.as_retriever() # 기본 값으로 상위 4개만 추출합니다.

# Retriever가 실제로 어떤 문서를 선택하는지 확인
# LangChain 방식으로는 보통 이걸 씁니다.

# get_relevant_documents()는 구버전 방식이고, 최신 버전에서는 invoke()를 써야 합니다
# docs = retriever._get_relevant_documents(query_document)
print('# 유사도가 높은 것 K를 추출합니다.(K의 기본 값은 4)')
docs = retriever.invoke(user_question)
for d in docs:
    print(d.page_content)


# 프롬프트 템플릿(카페 직원 역할 고정)
from langchain_core.prompts import ChatPromptTemplate

# 📌 교육 포인트
# {context} → Retriever가 찾아온 메뉴 설명
# {question} → 손님 질문
# RAG는 이 둘을 합쳐서 LLM에 전달

prompt = ChatPromptTemplate.from_template(
    # System 역할, 행동 규칙
    # Context : Retriever가 찾은 문서들이 들어오는 위치
    # question : 매번 달라지는 실제 사용자의 질문
    """
    너는 카페 직원이다.
    아래 정보를 참고해서 손님의 질문에 답해라.
    정보에 없는 내용은 추측하지 마라.

    카페 정보:
    {context}

    손님 질문:
    {question}
    """
)

# LLM + RAG 체인 구성(LCEL)
model = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0.3, max_tokens=100)
parser = StrOutputParser()

# rag_chain은 Retriever + Prompt + LLM + OutputParser를
# 하나의 실행 파이프라인(Chain)으로 연결한 객체
# "question": lambda x: x는 사용자가 키보드로 입력한 내용을 '질문으로 간주하겠다'라는 의미
rag_chain =(
    {
        "context": retriever,
        "question": lambda x: x
    }
    | prompt
    | model
    | parser
)

print('\n# 실행 예시(손님 질문)')
print(f'# 질문 내용 : {user_question}')
response = rag_chain.invoke(user_question)
print('\n# AI의 응답')
print(response)