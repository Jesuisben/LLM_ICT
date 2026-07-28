# Vector DB에 저장된 정보를 출력해 봅니다.
# python -X utf8 rag_02_read_vector_db.py > rag_02_read_vector_db.py.result.txt
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
########################################################################
# 임베딩 모델 생성
########################################################################
# OpenAIEmbeddings는 langchain_openai로 import 해야함
# -> from langchain_openai import OpenAIEmbeddings
embed_object = OpenAIEmbeddings(api_key=api_key)
########################################################################
# 저장된 Chroma DB 로딩
########################################################################
saved_path = "./rag_from_pdf_db"

vector_store = Chroma(
    persist_directory=saved_path,
    embedding_function=embed_object
)

print("DB 로딩 완료")
########################################################################
# 전체 데이터 조회
########################################################################
# ids 컬럼은 자동으로 읽어옴(문서 ID)
# "documents" : 문서 내용, "metadatas" : 메타 데이터, "embeddings" : 임베딩 벡터 정보
vector_info = vector_store.get(
    include=["documents", "metadatas", "embeddings"]
)

ids = vector_info["ids"]
documents = vector_info["documents"]
metadatas = vector_info["metadatas"]
embeddings_vector = vector_info["embeddings"]

print(f"총 데이터 개수 : {len(documents)}")

########################################################################
# 결과 출력
########################################################################
for idx in range(len(documents)):
    print(f"문서 번호 : {idx+1}")

    print(f"\nID : {ids[idx]}")

    print("\n문서의 내용 : ")
    print(documents[idx])

    print("\n메타 데이터 : ")
    print(metadatas[idx])

    print("\n임베딩 벡터의 일부 : ")
    print(embeddings_vector[idx][:10])

    print(f"\n벡터의 차원 수 : {len(embeddings_vector[idx])}")
########################################################################