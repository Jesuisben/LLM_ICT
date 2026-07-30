# ============================================================
# YouTube 검색 + GPT 요약 + 키워드 분석
# ============================================================
# Youtube 요약
# pip install youtube-search
# pip install youtube_transcript_api

import streamlit as st
import sys
from pathlib import Path
# ============================================================
# Project Root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0,str(PROJECT_ROOT))
# ============================================================
# Local Module Import
# ============================================================
from chapter07_search_engine.youtube.youtube_util import (
    search_youtube,
    load_all_caption
)

from chapter07_search_engine.youtube.video_util import (
    show_videos
)
# ============================================================
# Page
# ============================================================
st.set_page_config(
    page_title="YouTube Summary",
    page_icon="🎬",
    layout="wide"
)

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
# SideBar
# ============================================================
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
    use_container_width=True
)

# ============================================================
# Main
# ============================================================
if start_search:
    # --------------------------------------------------------
    # 검색
    # --------------------------------------------------------
    with st.spinner("Youtube 검색 중 ..."):
        videos = search_youtube(
            keyword, max_results
        )

    if not videos:
        st.warning("검색 결과가 없습니다.")
        st.stop()

    show_videos(videos)
    st.divider()
    # --------------------------------------------------------
    # 자막 읽기
    # --------------------------------------------------------
    with st.spinner("자막 다운로드 중 ..."):
        caption_videos = load_all_caption(videos)
    # --------------------------------------------------------
    # GPT 준비
    # --------------------------------------------------------

    # --------------------------------------------------------
    # 요약
    # --------------------------------------------------------

    # --------------------------------------------------------
    # 지원
    # --------------------------------------------------------
    pass

# ============================================================
# 임시
# ============================================================
def xxx():
    pass
