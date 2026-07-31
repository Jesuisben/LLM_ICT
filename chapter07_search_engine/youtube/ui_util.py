import streamlit as st


# ============================================================
# Page
# ============================================================
def set_page():
    st.set_page_config(
        page_title="YouTube Summary",
        page_icon="🎬",
        layout="wide"
    )


# ============================================================
# Title
# ============================================================
def draw_title():
    st.title("🎬 YouTube GPT Summary")

    st.write(
        """
검색어를 입력하면

- YouTube 검색
- 자막 다운로드
- GPT 요약
- 키워드 분석

을 수행합니다.
"""
    )

    st.divider()


# ============================================================
# Sidebar
# ============================================================
def draw_sidebar():

    st.sidebar.header("검색 옵션")

    keywords = [
        "생성형 AI",
        "ChatGPT",
        "Python",
        "LangChain",
        "Streamlit",
        "RAG",
        "LangGraph"
    ]

    keyword = st.sidebar.selectbox(
        "검색어 선택",
        keywords,
        index=3
    )

    max_results = st.sidebar.slider(
        "검색 개수",
        1,
        10,
        3
    )

    start_search = st.sidebar.button(
        "검색 시작",
        width="stretch"
    )

    return keyword, max_results, start_search


# ============================================================
# Summary Header
# ============================================================
def draw_summary_header():
    st.divider()
    st.header("📄 영상별 요약")


# ============================================================
# Keyword Header
# ============================================================
def draw_keyword_header():
    st.divider()


# ============================================================
# Message
# ============================================================
def show_no_result():
    st.warning("검색 결과가 없습니다.")
    st.stop()


def show_summary_complete():
    st.success("영상 요약 완료")


def show_analysis_complete():
    st.success("분석 완료")

# ===== End Of File ======================================================