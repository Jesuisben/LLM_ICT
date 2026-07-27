# =====================================================
# create_vector_db.py
# PDF 문서를 Vector DB(Chroma)에 저장하는 코드
# =====================================================
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
# =====================================================
# step01. PDF 로드
# =====================================================

print("\n==============================")
print("PDF 문서 로드")
print("==============================")

pdf_loader = PyMuPDFLoader("커피 매장 메뉴 및 이용 정보.pdf")

documents = pdf_loader.load()

print(f"로드된 문서 수: {len(documents)}")

# =====================================================
# step02. 문서 분할
# =====================================================

print("\n==============================")
print("문서 분할")
print("==============================")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"생성된 Chunk 수: {len(chunks)}")

# =====================================================
# step03. 임베딩 모델 생성
# =====================================================

print("\n==============================")
print("임베딩 모델 생성")
print("==============================")

embed_object = OpenAIEmbeddings()

# =====================================================
# step04. Chroma Vector DB 생성
# =====================================================

print("\n==============================")
print("Vector DB 생성 및 저장")
print("==============================")

saved_path = "./rag_from_pdf_db"

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embed_object,

    # 저장 폴더
    persist_directory=saved_path
)

print("Chroma DB 저장 완료")
print(f"저장 위치: {saved_path}")