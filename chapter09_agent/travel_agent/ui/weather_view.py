import streamlit as st


def show_weather(weather):
    # 날씨 출력 담당
    if weather is None:
        return

    if not weather.location:
        return

    st.subheader(
        "🌤 날씨 정보"
    )


    st.text(
        str(weather)
    )