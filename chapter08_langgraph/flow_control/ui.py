# Streamlit의 화면 UI 담당 파일

import streamlit as st


def draw_ui():

    st.title("LangGraph 흐름 제어 예제")

    login_success = st.checkbox(
        "로그인 성공",
        value=False
    )

    if not login_success: # 로그인을 하지 않는 경우, 장바구니에 상품이 있을 수 없음
        st.session_state.has_cart = False

    has_cart = st.checkbox(
        "장바구니에 상품이 있음",
        key="has_cart",
        disabled=not login_success # '로그인 성공' 체크 박스 미선택시 편집 불가능
    )

    return login_success, has_cart
