# =====================================================
# streamlit_rag.py
# Streamlit 기반 RAG 챗봇
# 참조 이미지 :
# =====================================================
import os, sys
import streamlit as st

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_community.vectorstores import Chroma

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

project_root = os.path.dirname(os.getcwd())
sys.path.insert(0, project_root)

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="RAG 챗봇",
    page_icon="☕",
    layout="wide"
)

st.title("☕ 카페 메뉴 RAG 챗봇")

# =====================================================
# Session State
# =====================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = InMemoryChatMessageHistory()

# =====================================================
# step01. 임베딩 모델
# =====================================================

@st.cache_resource
def load_embeddings():
    return OpenAIEmbeddings()

embed_object = load_embeddings()

# =====================================================
# step02. Chroma DB 로드
# =====================================================

@st.cache_resource
def load_vectorstore():

    saved_path = "./rag_from_pdf_db"

    vec_store = Chroma(
        persist_directory=saved_path,
        embedding_function=embed_object
    )

    return vec_store

vector_store = load_vectorstore()

# =====================================================
# step03. Prompt
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
# step04. LLM
# =====================================================

@st.cache_resource
def load_model():

    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        max_tokens=100
    )

    return model

model = load_model()

# =====================================================
# step05. 유사도 검색
# =====================================================

def get_context_with_score(question):

    docs_with_score = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    # score 오름차순 정렬
    # (낮을수록 더 유사)
    docs_with_score = sorted(
        docs_with_score,
        key=lambda x: x[1]
    )

    context_text = "\n\n".join([
        doc.page_content
        for doc, _ in docs_with_score
    ])

    return context_text, docs_with_score

# =====================================================
# step06. RAG 실행
# =====================================================

def run_rag(question):

    context, docs_with_score = get_context_with_score(question)

    chain = prompt | model | StrOutputParser()

    answer = chain.invoke({

        "context": context,

        "question": question,

        "chat_history":
            st.session_state.chat_history.messages
    })

    return answer, docs_with_score

# =====================================================
# 사용자 입력
# =====================================================

question = st.chat_input("질문을 입력하세요")

# =====================================================
# 질문 처리
# =====================================================

if question:

    # 사용자 질문 출력
    with st.chat_message("user"):
        st.write(question)

    # RAG 실행
    answer, docs_with_score = run_rag(question)

    # -------------------------------------------------
    # 검색 문서 출력
    # -------------------------------------------------

    st.subheader("검색된 문서")

    for idx, (doc, score) in enumerate(docs_with_score):

        with st.expander(f"문서 {idx+1}"):

            st.write(f"유사도 점수: {score:.4f}")

            st.write(doc.page_content)

    # -------------------------------------------------
    # AI 답변 출력
    # -------------------------------------------------

    with st.chat_message("assistant"):

        st.subheader("AI 답변")

        st.write(answer)

    # -------------------------------------------------
    # 메모리 저장
    # -------------------------------------------------

    st.session_state.chat_history.add_user_message(question)

    st.session_state.chat_history.add_ai_message(answer)