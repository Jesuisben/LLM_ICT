# RAG에 사용할 Pdf 파일 원본입니다.

import warnings

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# 안되는 사람은 pymupdf의 버전을 1.24.14로 교체하기
from langchain_community.document_loaders import PyMuPDFLoader

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
########################################################################
# PDF 문서 읽기
########################################################################
# PyMuPDFLoader 생성자로 객체 생성
pdf_loader = PyMuPDFLoader("커피 매장 메뉴 및 이용 정보.pdf")
documents = pdf_loader.load()
print(f"로딩된 문서 갯수 : {len(documents)}")
########################################################################
# 문서 분할
# document를 chunk로 만들기 위해 분할을 해야할때 사용
########################################################################
text_splitter = RecursiveCharacterTextSplitter(
    # 청크 크기
    chunk_size=300,
    # 청크 오버랩 (중복되게 이어 붙이는 부분)
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print(f"생성된 chunk의 갯수 : {len(chunks)}")
########################################################################
# 임베딩 모델 생성하기
########################################################################
# OpenAIEmbeddings는 langchain_openai로 import 해야함
# -> from langchain_openai import OpenAIEmbeddings
embed_object = OpenAIEmbeddings(api_key=api_key)
########################################################################
# Chroma Vector DB 생성
########################################################################
# 저장할 공간 만들기
saved_path = "./rag_from_pdf_db"
# Chroma는 langchain_chroma로 import
# 자바의 static 메소드 같은 것 (from_documents())
vectorstore = Chroma.from_documents(
    # documents 인자에 chunks 넣기
    documents=chunks,
    embedding=embed_object,
    persist_directory=saved_path
)
########################################################################
print("Chroma DB 저장 완료")
print(f"저장 위치 : {saved_path}")
########################################################################