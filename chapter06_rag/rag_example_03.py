"""
SQLite + FAISS + Streamlit

RAG Build

1. SQLite 선택
2. 문서 읽기
3. Embedding 생성
4. FAISS 저장
"""

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

st.title("📚 SQLite → FAISS Vector DB 생성")


# Session State
if "documents" not in st.session_state:
    st.session_state.documents = None

if "db_path" not in st.session_state:
    st.session_state.db_path = None


# 1. SQLite 선택
st.header("1. SQLite DB 선택")

st.write(f"현재 폴더 : {os.getcwd()}")

db_file = st.file_uploader(
    "SQLite 파일 선택",
    type=["db"]
)

if db_file:

    os.makedirs("temp", exist_ok=True)

    temp_db = os.path.join(
        "temp",
        db_file.name
    )

    with open(temp_db, "wb") as f:
        f.write(db_file.getbuffer())

    st.session_state.db_path = temp_db

    st.success("DB 선택 완료")


# 2. SQLite 읽기
st.header("2. SQLite 읽기")

if st.button("DB 읽기"):

    if st.session_state.db_path is None:
        st.warning("먼저 DB를 선택하세요.")

    else:
        documents = load_documents(
            st.session_state.db_path
        )

        st.session_state.documents = documents

        st.success(
            f"{len(documents)}개 문서 로드 완료"
        )


# 문서 출력
if st.session_state.documents:

    st.header("문서 목록")

    for i, doc in enumerate(st.session_state.documents, start=1):
        st.write(f"{i}. {doc}")

# 3. Embedding + FAISS 생성
st.header("3. Vector DB 생성")

if st.button("Embedding 생성 및 FAISS 저장"):
    if st.session_state.documents is None:
        st.warning("먼저 DB를 읽으세요.")
        st.stop()

    progress = st.progress(0)
    message = st.empty()

    message.write(
        "Embedding 생성..."
    )

    embed_object = OpenAIEmbeddings(
        api_key=api_key
    )

    progress.progress(30)


    message.write(
        "FAISS Index 생성..."
    )

    vectorstore = FAISS.from_texts(
        st.session_state.documents,
        embed_object
    )

    progress.progress(70)

    os.makedirs("vector_db", exist_ok=True)

    message.write( "Vector DB 저장..." )

    vectorstore.save_local(
        "vector_db"
    )

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