# =====================================================
# read_all_vector_db.py
# Chroma Vector DB의 전체 데이터 조회
# =====================================================
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
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
# step03. 전체 데이터 조회
# =====================================================

print("\n==============================")
print("Vector DB 전체 데이터 조회")
print("==============================")

# 현재 Chroma DB 안에 저장된 원문, 메타데이터, 벡터를 모두 확인하는 디버깅용 조회 명령
# include 옵션:
# documents : 문서 내용
# metadatas : 메타 데이터
# embeddings : 벡터 값
vector_info = vector_store.get(
    include=["documents", "metadatas", "embeddings"]
)

documents = vector_info["documents"]
metadatas = vector_info["metadatas"]
embeddings_data = vector_info["embeddings"]
ids = vector_info["ids"]

print(f"\n총 데이터 수: {len(documents)}")

# =====================================================
# step04. 결과 출력
# =====================================================

for idx in range(len(documents)):

    print("\n========================================")
    print(f"문서 번호: {idx+1}")
    print("========================================")

    # ID
    print(f"\nID:")
    print(ids[idx])

    # 문서 내용
    print(f"\n문서 내용:")
    print(documents[idx])

    # 메타데이터
    print(f"\n메타 데이터:")
    print(metadatas[idx])

    # 벡터 일부만 출력
    print(f"\n임베딩 벡터 일부:")
    print(embeddings_data[idx][:10])

    print(f"\n벡터 차원 수: {len(embeddings_data[idx])}")

print("\n==============================")
print("✅ 전체 조회 완료")
print("==============================")