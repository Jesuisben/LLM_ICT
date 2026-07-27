"""
rag_util.py

RAG 관련 기능

1. 문서 분할
2. Chroma Vector DB 생성
3. Vector DB 저장
4. Vector DB 로드
5. Retriever 생성
6. 문서 검색
"""

import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import Chroma


####################################################
# Chunk 생성
####################################################
def split_documents(
        documents,
        chunk_size=300,
        chunk_overlap=50
):
    """
    Document를 Chunk로 분할

    Parameters
    ----------
    documents : list[Document]

    chunk_size : int

    chunk_overlap : int

    Returns
    -------
    list[Document]
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=chunk_size,

        chunk_overlap=chunk_overlap

    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks


####################################################
# Embedding 생성
####################################################
def create_embedding():
    """
    OpenAI Embedding 생성

    Returns
    -------
    OpenAIEmbeddings
    """

    embedding = OpenAIEmbeddings()

    return embedding


####################################################
# Chroma 생성
####################################################
def create_vectorstore(
        chunks,
        embedding=None,
        persist_directory="vector_db"
):
    """
    Chroma Vector DB 생성

    Parameters
    ----------
    chunks : list[Document]

    embedding : OpenAIEmbeddings

    persist_directory : str

    Returns
    -------
    Chroma
    """

    if embedding is None:

        embedding = create_embedding()

    vectorstore = Chroma.from_documents(

        documents=chunks,

        embedding=embedding,

        persist_directory=persist_directory

    )

    return vectorstore


####################################################
# Vector DB Load
####################################################
def load_vectorstore(
        persist_directory="vector_db",
        embedding=None
):
    """
    저장된 Chroma DB 읽기

    Returns
    -------
    Chroma
    """

    if embedding is None:

        embedding = create_embedding()

    vectorstore = Chroma(

        persist_directory=persist_directory,

        embedding_function=embedding

    )

    return vectorstore


####################################################
# Retriever 생성
####################################################
def create_retriever(
        vectorstore,
        top_k=4
):
    """
    Retriever 생성

    Parameters
    ----------
    vectorstore : Chroma

    top_k : int

    Returns
    -------
    Retriever
    """

    retriever = vectorstore.as_retriever(

        search_kwargs={

            "k": top_k

        }

    )

    return retriever


####################################################
# 문서 검색
####################################################
def search_documents(
        retriever,
        question
):
    """
    Retriever 검색

    Parameters
    ----------
    retriever

    question : str

    Returns
    -------
    list[Document]
    """

    docs = retriever.invoke(
        question
    )

    return docs


####################################################
# Vector DB 삭제
####################################################
def delete_vectorstore(
        persist_directory="vector_db"
):
    """
    Vector DB 삭제

    Returns
    -------
    bool
    """

    if not os.path.exists(
            persist_directory
    ):

        return False

    import shutil

    shutil.rmtree(
        persist_directory
    )

    return True