# =====================================================================
# 이 파일은 streamlit UI Framework로 UI를 구성하는 파일입니다.
# =====================================================================
import streamlit as st

# =====================================================================
# 페이지 설정
# =====================================================================
def setup_page():
    ''' 페이지 기본 설정 '''
    st.set_page_config(
        page_title="DuckDuckGo News Search",
        page_icon="🔍",
        layout="wide",
    )

    st.title("🔍 DuckDuckGo + LangChain News Search")
    st.markdown("---")

# =====================================================================
# 사이드 바 설정
# =====================================================================
def show_sidebar():
    with st.sidebar:

        st.header("⚙ 검색 옵션")

        region = st.selectbox(
            "Region",
            [
                "kr-ko",
                "us-en",
                "jp-jp",
            ],
            index=0,
        )

        news_only = st.checkbox(
            "News Search",
            value=True,
        )

        max_tokens = st.slider(
            "Max Completion Tokens",
            50,
            500,
            150,
        )

    return region, news_only, max_tokens
# =====================================================================
# 사용자 질문 입력란
# =====================================================================
def user_question():
    question = st.text_input(
        "질문을 입력하세요.",
        value="최근 MZ세대의 주요 소비 트렌드는 무엇인가요?",
    )

    return question

# =====================================================================
# 스피너 : 진행 상황을 알려 주는 UI(동글 동글 돌아감)
# =====================================================================
def show_spinner(text):
    return st.spinner(text)

# ============================================================
# DuckDuckGo 검색 결과
# ============================================================
def show_search_result(docs):
    st.subheader("① DuckDuckGo 검색 결과")

    st.text_area(
        "Search Result",
        docs,
        height=250,
    )

# ============================================================
# 기사 링크
# ============================================================
def show_links(link_list):
    st.subheader("② 기사 링크")

    if len(link_list) == 0:
        st.info("검색된 링크가 없습니다.")
        return

    for idx, link in enumerate(link_list, start=1):
        st.markdown(f"{idx}. {link}")
# ============================================================
# 기사 내용
# ============================================================

def show_articles(article_list):

    st.subheader("③ 기사 내용")

    if len(article_list) == 0:
        st.info("기사 내용이 없습니다.")
        return

    for idx, article in enumerate(article_list, start=1):

        with st.expander(f"기사 {idx}"):

            st.write(article)


# ============================================================
# GPT 답변
# ============================================================

def show_answer(answer):

    st.subheader("④ GPT 답변")

    st.success(answer.content)


# ============================================================
# Token 사용량
# ============================================================

def show_token_usage(answer):

    usage = answer.response_metadata["token_usage"]

    st.subheader("⑤ Token Usage")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Prompt",
        usage["prompt_tokens"],
    )

    col2.metric(
        "Completion",
        usage["completion_tokens"],
    )

    col3.metric(
        "Total",
        usage["total_tokens"],
    )

# ============================================================
# 메시지 출력
# ============================================================

def show_message(msg):

    st.info(msg)


def show_error(msg):

    st.error(msg)


def show_success(msg):

    st.success(msg)


# ============================================================
# 구분선
# ============================================================

def line():

    st.divider()

# ======= End Of File =================================================