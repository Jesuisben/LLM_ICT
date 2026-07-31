# =====================================================================
# DuckDuckGo + Web Crawler + LangChain RAG
# 실행 : streamlit run web_search_streamlit.py
# =====================================================================
import sys
from pathlib import Path

import streamlit as st

from langchain_core.chat_history import InMemoryChatMessageHistory
# ============================================================
# Project Root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0,str(PROJECT_ROOT))
# =====================================================================
# Local Module Import
# =====================================================================
from chapter07_search_engine.duckduckgo.ui_util import (
    setup_page,
    show_sidebar,
    user_question,
    show_spinner,
    show_search_result,
    show_links,
    show_articles,
    show_answer,
    show_token_usage,
    show_error,
    line,
)

from chapter07_search_engine.duckduckgo.search_util import (
    search_news,
    search,
    extract_links
)

from chapter07_search_engine.duckduckgo.crawler_util import (
    get_articles,
    merge_articles
)

from chapter07_search_engine.duckduckgo.llm_util import (
    create_model,
    create_chain
)
# =====================================================================
# Constant
# =====================================================================
CHAT_HISTORY = 'chat_history' # 메시지 주고 받은 이력의 저장소 이름
# =====================================================================
# Session State
# =====================================================================
def init_state():
    if CHAT_HISTORY not in st.session_state:
        st.session_state[CHAT_HISTORY] = (
            InMemoryChatMessageHistory()
        )
# =====================================================================
# Main
# =====================================================================
def main():
    setup_page()

    init_state()

    region, news_only, max_tokens = show_sidebar()

    question = user_question()

    if st.button(
            "🔍 검색 + GPT 분석",
            type="primary"
    ):
        try:
            # -------------------------------------------------------------
            # Search
            # -------------------------------------------------------------
            with show_spinner('DuckDuckGo 뉴스 검색 중...'):
                # st.write('a')

                if news_only: # 오직 news만 검색
                    docs = search_news(
                        question,
                        region=region
                    )

                else:
                    docs = search(question)
            # end with

            show_search_result(docs)

            line() # 구분선

            # -------------------------------------------------------------
            # URL Extract
            # -------------------------------------------------------------
            link_list = extract_links(docs)

            show_links(link_list)

            line()
            # -------------------------------------------------------------
            # Crawling
            # -------------------------------------------------------------
            with show_spinner('기사 내용을 수집(Crawling) 중...'):
                article_list = get_articles(link_list)

            show_articles(article_list)

            line()
            # -------------------------------------------------------------
            # Context 생성
            # -------------------------------------------------------------
            context = merge_articles(article_list)

            if not context:
                st.warning('기사 내용을 가져 오지 못했습니다.')

                return
            # -------------------------------------------------------------
            # LLM 호출
            # -------------------------------------------------------------
            with show_spinner('GPT 답변 생성 중...'):
                model = create_model(max_tokens=max_tokens)

                chain = create_chain(model)

                # 사용자의 질문 내용과 context를 chain에 넘겨줘 응답을 받습니다.
                answer = chain.invoke({
                    'messages':[('human', question)],
                    'context':context[:12000] # 문자수 12000개
                })
            # -------------------------------------------------------------
            # History 저장
            # -------------------------------------------------------------
            history = st.session_state[CHAT_HISTORY]

            history.add_user_message(question)

            history.add_ai_message(answer.content)
            # -------------------------------------------------------------
            # 결과 출력
            # -------------------------------------------------------------
            show_answer(answer)

            show_token_usage(answer)

        except Exception as err:
            show_error(f'오류 발생 : {err}')
# end def main():

# =====================================================================
# 최초 진입점(Entry Point)
# =====================================================================
if __name__ == '__main__':
    main()
# ======= End Of File =================================================