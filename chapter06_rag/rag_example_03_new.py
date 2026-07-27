import os
import sys
import streamlit as st

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

project_root = os.path.dirname(os.getcwd())
sys.path.insert(0, project_root)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utility.env_util import get_api_key
from rag_example_02 import load_documents

api_key = get_api_key("OPENAI_API_KEY")

# Streamlit 설정
st.set_page_config(
    page_title="RAG Build",
    layout="wide"
)

st.title("SQLite → FAISS Vector DB 생성")

print("# Session State 설정")
# "documents" : SQLite DB에서 읽어온 텍스트 형식의 목록 리스트(Document)
if "documents" not in st.session_state:
    # streamlit의 내부 공간인 session_state에 documents가 없으면
    # 일단 None을 넣어서 공간을 확보함
    st.session_state.documents = None

# "db_path" : Sqlite DB의 경로와 이름 정보
if "db_path" not in st.session_state:
    st.session_state.db_path = None

st.header("1. SQLite DB 선택")

# wd : working directory (리눅스에서 pwd하면 현재 작업하는 공간을 보여줌)
# cwd(Current Working Directory) : 현재 작업 폴더
st.write(f"현재 폴더 : {os.getcwd()}")

db_file = st.file_uploader("SQLite 파일 선택", type=["db"])

if db_file:
    # 선택한 sqlite db 파일의 복사본을 만들고, db_path의 값을 설정합니다.
    os.makedirs("temp", exist_ok=True)

    # join() : 매개변수들을 \ 역슬래쉬로 연결해서 하나의 문자열 생성
    # -> f"temp\{db_file.name}" -> "temp\cafe.db"
    temp_db = os.path.join("temp", db_file.name)

    # mode="wb" : 원래 텍스트 파일들을 작업할때 wt(text)를 했는데
    # db 파일은 바이너리 파일이라서 "wb"를 사용해야함
    with open(temp_db, mode="wb") as myfile :
        myfile.write(db_file.getbuffer())

    st.session_state.db_path = temp_db

    st.success("DB 선택 완료")

st.header("2. SQLite 읽기")

if st.button("DB 읽기"):
    if st.session_state.db_path is None:
        st.warning("먼저 DB를 선택하세요.")

    else:
        documents = load_documents(
            st.session_state.db_path
        )

        st.session_state.documents = documents

        st.success(f"{len(documents)} 개 문서 로드 완료")
    # end if

# 문서 출력
if st.session_state.documents:
    st.header("문서 목록")

    for idx, doc in enumerate(st.session_state.documents, start=1):
        st.write(f"{idx}. {doc}")

# 3. Embedding + FAISS 생성
st.header("3. Vector DB 생성")

if st.button("Embedding 생성 및 FAISS 저장"):
    if st.session_state.documents is None:
        st.warning("먼저 DB를 읽으세요.")
        st.stop()
    # end if

    # 진행바
    progress = st.progress(0) # 0%로 시작
    message = st.empty()


    # Embedding : 문자를 숫자로 변환
    message.write("Embedding 생성 ...")

    # embed_object는 임베딩 객체를 의미
    embed_object = OpenAIEmbeddings(api_key=api_key)

    progress.progress(30) # Embedding 과정이 끝나면 30% 진행했다고 표시함


    # FAISS (벡터 데이터)
    message.write("FAISS Index 생성 ...")

    vectorstore = FAISS.from_texts(
        st.session_state.documents,
        embed_object
    )

    progress.progress(70)


    # Vector DB
    VECTOR_DIR = "vector_db"
    os.makedirs(VECTOR_DIR, exist_ok=True)

    message.write("Vector DB 저장...")

    vectorstore.save_local(VECTOR_DIR)

    progress.progress(100)

    message.success(
        "Vector DB 생성 완료"
    )

    st.success(
        """
FAISS 저장 완료

vector_db/
 ├── index.faiss
 └── index.pkl
"""
    )

# end if