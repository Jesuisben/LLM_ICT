# rag_04_01_chatbot_streamlit(최신 질문 내용만 보여 주기).png

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

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
########################################################################
# 페이지 설정
########################################################################
st.set_page_config(
    page_title="RAG 챗봇",
    page_icon="☕",
    layout="wide"
)

st.title("☕ 카페 메뉴 RAG 챗봇")
########################################################################
# Session State
########################################################################
# 대화 내용 히스토리를 위한 상수
CHAT_HISTORY = "chat_history"

# InMemoryChatMessageHistory : 대화 내용을 메모리에 저장시키는 단순한 클래스
if "chat_history" not in st.session_state:
    st.session_state.chat_history = InMemoryChatMessageHistory()
########################################################################
# 임베딩 모델
########################################################################
# 비용이 들어가는 항목중 재사용이 필요한 항목은 캐싱하라.
@st.cache_resource
def load_embeddings(my_key):
    return OpenAIEmbeddings(api_key=my_key)

embed_object = load_embeddings(api_key)
########################################################################
# Chroma DB 로드
########################################################################
@st.cache_resource
def load_vectorstore():
    saved_path = "./rag_from_pdf_db"

    vec_store = Chroma(
        persist_directory=saved_path,
        embedding_function=embed_object
    )
    return vec_store

vector_store = load_vectorstore()
########################################################################
# Prompt
########################################################################
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """당신은 카페 직원입니다.
        반드시 제공된 문서의 내용만을 참조하여 답변해 주세요."""
    ),
    MessagesPlaceholder(variable_name=CHAT_HISTORY),
    (
        "human",
        "카페 정보:\n{context}\n\n질문 :\n{question} "
    )
])
########################################################################
# LLM 모델
########################################################################
@st.cache_resource
def load_model():
    somemodel = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        api_key=api_key,
        max_completion_tokens=100
    )
    return somemodel

model = load_model()
########################################################################
# 파서 객체 생성
########################################################################
str_parser = StrOutputParser()
########################################################################
# 유사도 검색
########################################################################
def get_context_with_score(user_question):
    # 사용자의 질문과 유사한 문서를 k개 읽어 옵니다.
    docs_with_score = vector_store.similarity_search_with_score(
        query=user_question,
        k=3
    )

    # x[0] : 문서, x[1] : 유사도 점수
    # 유사도 점수를 사용하여 오름차순 정렬
    # 주의 : Chroma는 기본적으로 거리를 반환합니다.(가까울수록 유사하다고 봄)
    docs_with_score = sorted(
        docs_with_score,
        key=lambda x: x[1]
    )

    # 반복문에서의 doc은 x[0]은 문서
    context_text = "\n\n".join([
        doc.page_content for doc, _ in docs_with_score
    ])

    return context_text, docs_with_score
########################################################################
# RAG 실행을 위한 함수 작성
########################################################################
def run_rag(user_question):
    # rag_context는 사실상 context_text과 같음
    rag_context, rag_docs_score = get_context_with_score(user_question)

    # langchain으로 chain을 생성
    chain = prompt | model | str_parser

    answer = chain.invoke({
        "context": rag_context,
        "question": user_question,
        CHAT_HISTORY: st.session_state[CHAT_HISTORY].messages
    })


    return answer, rag_docs_score
########################################################################
# 사용자 질문
########################################################################
# 아메리카노랑 잘 어울리는 디저트를 추천해 주세요.
question = st.chat_input("질문을 입력해 주세요.")
########################################################################
# 질문에 대한 처리
########################################################################
if question:
    with st.chat_message("user"):
        st.write(question)

    answer, docs_with_score = run_rag(question)

    st.subheader("검색된 문서")
    for idx, (doc, score) in enumerate(docs_with_score, start=1):
        # st.expander : 토글 확장
        with st.expander(f"문서 {str(idx).zfill(2)}"):
            st.write(f"유사도 점수 : {score:.4f}")
            st.write(doc.page_content)

    # AI의 답변
    with st.chat_message("assistant"):
        st.subheader("AI의 답변")
        st.write(answer)

    # 메모리에 Message 저장하기
    # 기억해야 할 메소드 : add_user_message() / add_ai_message()
    st.session_state[CHAT_HISTORY].add_user_message(question)
    st.session_state[CHAT_HISTORY].add_ai_message(answer)
########################################################################
# 사이드 바
########################################################################
with st.sidebar:
    if st.button("메모리 보기"):
        st.subheader("Chat History")

        for idx, msg in enumerate(st.session_state[CHAT_HISTORY].messages, start=1):
            st.write(f"[{idx}] {msg.type} : {msg.content}")
########################################################################