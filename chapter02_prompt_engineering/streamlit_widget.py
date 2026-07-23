import streamlit as st

st.set_page_config(
    page_title="Streamlit 첫 예제",
    page_icon="🎈",
    layout="centered"
)

st.title("🎈 Hello Streamlit")
st.write("Streamlit 앱이 정상적으로 실행되고 있습니다.")

st.divider()

st.header("📝 입력 위젯 데모")

name = st.text_input("이름")
age = st.number_input("나이", 0, 120, 25)
lang = st.selectbox("주 사용 언어", ["Python", "R", "C++"])

if st.button("확인"):
    st.success("입력이 완료되었습니다.")
    st.write("### 입력 결과")
    st.write(f"**이름** : {name}")
    st.write(f"**나이** : {age}")
    st.write(f"**언어** : {lang}")

# import streamlit as st
#
# st.header("입력 위젯 데모")
#
# name = st.text_input("이름을 입력하세요")
# age = st.number_input("나이", min_value=0, max_value=120, value=25)
# lang = st.selectbox("언어 선택", ["Python", "R", "C++"])
# submit = st.button("확인")
#
# if submit:
#     st.success(f"{name}님은 {age}세이며, {lang}을(를) 사용합니다.")