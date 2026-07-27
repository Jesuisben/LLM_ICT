"""
prompt_util.py

Prompt + LLM + RAG Chain

1. Prompt 생성
2. LLM 생성
3. Output Parser 생성
4. RAG Chain 생성
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_openai import ChatOpenAI

from utility.env_util import get_api_key


####################################################
# Prompt
####################################################
def create_prompt():
    """
    ChatPromptTemplate 생성

    Returns
    -------
    ChatPromptTemplate
    """

    prompt = ChatPromptTemplate.from_messages(

        [

            (
                "system",

                """
너는 친절한 카페 직원이다.

반드시 아래 규칙을 지켜라.

1. 제공된 카페 정보만 사용한다.
2. 모르는 내용은 추측하지 않는다.
3. 친절하고 간결하게 답변한다.
"""
            ),

            MessagesPlaceholder(
                variable_name="chat_history"
            ),

            (
                "human",

                """
카페 정보

{context}


질문

{question}
"""
            )

        ]

    )

    return prompt


####################################################
# LLM
####################################################
def create_llm(
        model_name="gpt-4o",
        temperature=0.3,
        max_tokens=500
):
    """
    ChatOpenAI 생성

    Parameters
    ----------
    model_name : str

    temperature : float

    max_tokens : int

    Returns
    -------
    ChatOpenAI
    """

    api_key = get_api_key(
        "OPENAI_API_KEY"
    )

    llm = ChatOpenAI(

        api_key=api_key,

        model=model_name,

        temperature=temperature,

        max_completion_tokens=max_tokens

    )

    return llm


####################################################
# Output Parser
####################################################
def create_parser():
    """
    문자열 Parser 생성
    """

    return StrOutputParser()


####################################################
# RAG Chain
####################################################
def create_rag_chain(
        retriever,
        chat_history
):
    """
    RAG Chain 생성

    Parameters
    ----------
    retriever

    chat_history

    Returns
    -------
    Runnable
    """

    prompt = create_prompt()

    llm = create_llm()

    parser = create_parser()

    rag_chain = (

        {

            "context": retriever,

            "question": lambda x: x,

            "chat_history":
                lambda x: chat_history.messages

        }

        | prompt

        | llm

        | parser

    )

    return rag_chain