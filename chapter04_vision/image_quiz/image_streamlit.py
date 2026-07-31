# =====================================================================
# Image Quiz 메인 모듈
# =====================================================================
import sys
from pathlib import Path

import streamlit as st

from langchain_core.chat_history import InMemoryChatMessageHistory

IMAGE_DIR = "images" # 이미지들이 들어 있는 디렉토리
IMAGE_QUIZ = 'quiz'
# ============================================================
# Project Root
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0,str(PROJECT_ROOT))
# =====================================================================
# Local Module Import
# =====================================================================
from chapter04_vision.image_quiz.ui_util import (
    setup_page,
    draw_title,
    draw_sidebar,
    select_image,
    show_image,
    show_quiz,
    download_md
)

from chapter04_vision.image_quiz.image_util import (
    get_image_list,
    create_all_quiz
)

from chapter04_vision.image_quiz.image_quiz import (
    image_quiz
)

from chapter04_vision.image_quiz.file_util import (
    make_markdown, load_descriptions
)
# =====================================================================
# Main
# =====================================================================
def main():
    setup_page()

    draw_title()

    options = draw_sidebar()

    image_list = get_image_list(IMAGE_DIR)

    # -----------------------
    # 모든 이미지 생성
    # -----------------------
    if options["create_all"]: # '모든 이미지 문제 생성' 버튼이 클릭됨
        with st.spinner("전체 이미지 분석 중..."):
            results = create_all_quiz(
                image_list
            )

            st.session_state.results = results

    # -----------------------
    # 개별 이미지
    # -----------------------
    descriptions = load_descriptions('combo_list.txt')
    # print(descriptions)

    selected_image = select_image(image_list, descriptions)

    if selected_image is not None:
        show_image(selected_image)

    st.session_state.pop(IMAGE_QUIZ, None)

    if st.button("문제 생성"):
        quiz = image_quiz(str(selected_image))

        st.session_state[IMAGE_QUIZ] = quiz

    if IMAGE_QUIZ in st.session_state:
        # options["show_answer"] : '정답 보기' 체크 박스 상태
        show_quiz(
            st.session_state[IMAGE_QUIZ],
            options["show_answer"]
        )

    # -----------------------
    # MD 저장
    # -----------------------
    if "results" in st.session_state:
        md = make_markdown(st.session_state.results)

        download_md(md)
# end def main():
# =====================================================================
# 최초 진입점(Entry Point)
# =====================================================================
if __name__ == '__main__':
    main()
# ======= End Of File =================================================