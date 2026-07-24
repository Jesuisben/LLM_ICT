import streamlit as st

# Streamlit 페이지의 설정
st.set_page_config(
    # 페이지의 브라우저 탭 제목
    page_title="Streamlit 첫 예제",

    # 페이지의 브라우저 탭 아이콘
    page_icon="🎈",

    # 페이지의 화면 너비 설정
    layout="centered"
)

# LLM(실습).pdf (P.21)
# 페이지 상단에 큰 제목을 출력
st.title("Hello Streamlit~")

# 제목 아래에 일반 텍스트 출력
st.write("Streamlit 앱이 정상적으로 동작하고 있습니다.")

# 가로 구분선 생성
st.divider()

# 중간 크기의 제목을 출력
st.header("입력 위젯 데모")

# 사용자에게 문자열을 입력받는 텍스트 입력 위젯
# React의 <input type="text">와 비슷한 역할
name = st.text_input("이름")

# number_input('나이', 최소값, 최대값, 보여지는값)
age = st.number_input("나이", 0, 120, 25)

# 여러 선택지 중 하나를 선택하는 드롭다운 위젯
# HTML의 <select> 또는 콤보박스와 비슷한 역할
lang = st.selectbox("주 사용 언어", ["Python", "R", "Java", "C++"])

# falsy, truthy 개념
# st.button()은 버튼을 클릭한 실행에서 True를 반환
if st.button("확인"):
    # 성공 메시지를 초록색 알림 상자 형태로 화면에 출력하는 함수
    st.success("입력이 완료되었습니다.")
    # 일반 텍스트 출력 (마크다운 문법이 적용되어 ###을 이용하면 크기가 커짐)
    st.write("### 입력 결과")
    # 마크다운 문법이 적용되어 **을 사용하면 굵은 글씨가 됨
    st.write(f"**이름** : {name}")
    st.write(f"**나이** : {age}")
    st.write(f"**언어** : {lang}")
    st.success(f"{name}님은 {age}세이며, {lang}을(를) 사용합니다.")