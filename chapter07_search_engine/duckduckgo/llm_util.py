# ============================================================
# Chat Open AI 관련 유틸리티 모듈입니다.
# ============================================================
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from utility.env_util import get_api_key
# ============================================================
# Open AI 모델을 생성하는 함수
# ============================================================
def create_model(
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.3,
    max_tokens: int = 150
):
    api_key = get_api_key("OPENAI_API_KEY")

    model = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
        max_completion_tokens=max_tokens
    )

    return model
# ============================================================
# Chain을 생성하는 함수
# ============================================================
def create_chain(
    model=None
):
    if model is None:
        model = create_model()

        prompt = create_prompt()

        # parser = StrOutputParser()

        chain = prompt | model #| parser

        return chain
# ============================================================
# PromptTemplate를 생성하는 함수
# ============================================================
def create_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
사용자의 질문에 대해 아래 Context를 참고하여
정확하고 이해하기 쉽게 답변해 주세요.

Context
-------
{context}
                """,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt