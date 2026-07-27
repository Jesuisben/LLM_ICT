"""
SQLite RAG Search

1. FAISS Vector DB Load
2. Retriever Search
3. Cosine Similarity
4. GPT RAG Answer
"""

import os
import sys
import numpy as np
import streamlit as st

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 프로젝트 경로
project_root = os.path.dirname(os.getcwd())
sys.path.insert(0, project_root)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utility.env_util import get_api_key


# API Key
api_key = get_api_key("OPENAI_API_KEY")


# Streamlit 설정
st.set_page_config(
    page_title="RAG Search",
    layout="wide"
)

st.title("🔎 FAISS 기반 RAG 검색")


# Session State
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "embedding" not in st.session_state:
    st.session_state.embedding = None


# Vector DB Load
st.header("1. Vector DB 불러오기")

vector_path = "vector_db"

if st.button("Vector DB Load"):

    if not os.path.exists(vector_path):
        st.error("vector_db 폴더가 없습니다.")
        st.stop()

    embed_object = OpenAIEmbeddings(
        api_key=api_key
    )

    vectorstore = FAISS.load_local(
        vector_path,
        embed_object,
        allow_dangerous_deserialization=True
    )

    st.session_state.vectorstore = vectorstore
    st.session_state.embedding = embed_object

    st.success("Vector DB 로드 완료")


if st.session_state.vectorstore:
    st.info("FAISS Vector DB 준비 완료")


# 질문 입력
st.header("2. 질문 입력")

question = st.text_input(
    "질문을 입력하세요",
    value="딸기 치즈케이크와 잘 어울리는 음료를 추천해 주세요"
)


top_k = st.slider("검색 문서 개수 (Top-K)", 1, 10, 4)

def cosine_similarity(qv, dv):
    return np.dot(qv, dv) / (
        np.linalg.norm(qv) *
        np.linalg.norm(dv)
    )


# 검색 실행
if st.button("검색하기"):
    if st.session_state.vectorstore is None:
        st.error("먼저 Vector DB를 Load 하세요.")
        st.stop()

    # Retriever
    retriever = st.session_state.vectorstore.as_retriever(
        search_kwargs={"k": top_k}
    )

    # 문서 검색
    docs = retriever.invoke(question)

    # 검색 결과
    st.header("3. 검색 결과")

    with st.expander(
        "검색된 문서 보기",
        expanded=True
    ):

        for i, doc in enumerate(docs, 1):
            st.write(
                f"문서 {i}: {doc.page_content}"
            )

    # Similarity
    st.header("4. Cosine Similarity")

    query_vector = (
        st.session_state.embedding
        .embed_query(question)
    )

    for i, doc in enumerate(docs, 1):

        doc_vector = (
            st.session_state.embedding
            .embed_query(doc.page_content)
        )

        score = cosine_similarity(
            query_vector,
            doc_vector
        )

        st.write(f"문서 {i} Similarity : {score:.4f}")

    # RAG Prompt
    st.header("5. GPT 답변")

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = ChatPromptTemplate.from_template(
        """
너는 카페 직원이다.

아래 정보를 참고해서 답변하세요.
없는 내용은 추측하지 마세요.

[카페 정보]
{context}

[질문]
{question}
"""
    )

    model = ChatOpenAI(
        api_key=api_key,
        model="gpt-4o",
        temperature=0.3
    )

    chain = ( prompt | model | StrOutputParser())


    answer = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    st.success(answer)