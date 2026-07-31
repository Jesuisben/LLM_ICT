# =====================================================================
# Streamlit UI 관리
# =====================================================================
import streamlit as st

from chapter04_vision.image_quiz.image_util import image_count


# =====================================================================
# 페이지 기본 설정
# =====================================================================
def setup_page():
    st.set_page_config(
        page_title="GPT Vision Image Quiz",
        page_icon="🖼️",
        layout="wide"
    )
# =====================================================================
def draw_title():
    st.title("🖼️ GPT Vision 이미지 퀴즈 생성기")
# =====================================================================
# 사이드 바 설정
# =====================================================================
def draw_sidebar():
    st.sidebar.header("⚙️ 옵션")

    create_all = st.sidebar.button("📚 모든 이미지 문제 생성", width='stretch')

    show_answer = st.sidebar.checkbox("정답 보기", value=True)

    save_md = st.sidebar.button("💾 MD 파일 저장", width='stretch')

    return {
        "create_all": create_all,
        "show_answer": show_answer,
        "save_md": save_md
    }
# =====================================================================
# 콤보 박스에 선택된 이미지 정보를 반환해주는 함수
# =====================================================================
def select_image(image_list, descriptions):
    names = [img.name for img in image_list]

    names.insert(0, "이미지를 선택하세요")

    selected = st.selectbox("이미지 선택", names, format_func=lambda x: descriptions.get(x, x), width=600)

    if selected == "이미지를 선택하세요":
        return None

    for img in image_list:
        if img.name == selected:
            return img
# =====================================================================
# 선택된 이미지를 화면에 보여 주는 함수
# =====================================================================
def show_image(image):
    st.image(
        image,
        width=600
    )
# =====================================================================
# 세션 내에 있는 정답 퀴즈(session_in_quiz) 정보에서
# 체크 박스의 on/off 설정(show_answer)에 따라 정답을 보이거나 숨겨주는 함수
# =====================================================================
def show_quiz(session_in_quiz, show_answer=True):
    if show_answer: # 정답을 보여 주는  경우
        st.markdown(session_in_quiz)

    else:
        hide_answer = remove_answer(session_in_quiz)
        st.markdown(hide_answer)
# =====================================================================
# sentense내에서 정답 부분만 제거해주는 함수
# =====================================================================
def remove_answer(sentense):
    if "정답:" in sentense:
        return sentense.split("정답:")[0]

    return sentense
# =====================================================================
# Markdown 파일을 다운로드할 수 있도록 해주는 함수
# =====================================================================
def download_md(content):
    return st.download_button(
        label="📥 Markdown 다운로드",
        data=content,
        file_name="image_quiz.md",
        mime="text/markdown"
    )
# =====================================================================