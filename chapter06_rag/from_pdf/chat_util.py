"""
chat_util.py

대화 기록 관리

1. Chat History 생성
2. 사용자 메시지 저장
3. AI 메시지 저장
4. 대화 기록 조회
5. 대화 기록 초기화
"""

from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)


####################################################
# Chat History 생성
####################################################
def create_chat_history():
    """
    대화 기록 객체 생성

    Returns
    -------
    InMemoryChatMessageHistory
    """

    return InMemoryChatMessageHistory()


####################################################
# 사용자 메시지 저장
####################################################
def add_user_message(
        chat_history,
        message
):
    """
    사용자 메시지 저장
    """

    chat_history.add_user_message(
        message
    )


####################################################
# AI 메시지 저장
####################################################
def add_ai_message(
        chat_history,
        message
):
    """
    AI 메시지 저장
    """

    chat_history.add_ai_message(
        message
    )


####################################################
# 대화 기록 조회
####################################################
def get_messages(
        chat_history
):
    """
    저장된 메시지 반환

    Returns
    -------
    list
    """

    return chat_history.messages


####################################################
# 대화 기록 초기화
####################################################
def clear_chat_history(
        chat_history
):
    """
    대화 기록 삭제
    """

    chat_history.clear()