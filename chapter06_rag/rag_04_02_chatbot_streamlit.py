# =====================================================
# streamlit_rag_chat.py
# ChatGPT 스타일 Streamlit RAG 챗봇
# =====================================================
import os, sys
import streamlit as st

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_community.vectorstores import Chroma

from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.output_parsers import StrOutputParser

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
# Session State 초기화
# =====================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = InMemoryChatMessageHistory()

# 화면 출력용 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# step01. 임베딩 모델
# =====================================================

@st.cache_resource
def load_embeddings():
    return OpenAIEmbeddings()

embeddings = load_embeddings()

# =====================================================
# step02. Chroma DB 로드
# =====================================================

@st.cache_resource
def load_vectorstore():

    saved_path = "./rag_from_pdf_db"

    vectorstore = Chroma(
        persist_directory=saved_path,
        embedding_function=embeddings
    )

    return vectorstore

vectorstore = load_vectorstore()

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

    return ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        max_tokens=100
    )

model = load_model()

# =====================================================
# step05. Context 생성
# =====================================================

def get_context(question):

    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    context_text = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    return context_text

# =====================================================
# step06. RAG 실행
# =====================================================

def run_rag(question):

    context = get_context(question)

    chain = prompt | model | StrOutputParser()

    answer = chain.invoke({

        "context": context,

        "question": question,

        "chat_history":
            st.session_state.chat_history.messages
    })

    return answer

# =====================================================
# 이전 대화 출력
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# =====================================================
# 사용자 입력
# =====================================================

question = st.chat_input("질문을 입력하세요")

# =====================================================
# 질문 처리
# =====================================================

if question:

    # -------------------------------------------------
    # 사용자 질문 저장
    # -------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # 사용자 질문 출력
    with st.chat_message("user"):
        st.write(question)

    # -------------------------------------------------
    # AI 답변 생성
    # -------------------------------------------------

    answer = run_rag(question)

    # -------------------------------------------------
    # AI 답변 저장
    # -------------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # AI 답변 출력
    with st.chat_message("assistant"):
        st.write(answer)

    # -------------------------------------------------
    # LangChain 메모리 저장
    # -------------------------------------------------

    st.session_state.chat_history.add_user_message(question)

    st.session_state.chat_history.add_ai_message(answer)