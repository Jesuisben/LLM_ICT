import streamlit as st


def show_hotel(hotel_list):
    # 호텔 출력 담당
    if not hotel_list:
        return


    st.subheader(
        "🏨 호텔 정보"
    )


    st.text(
        str(hotel_list)
    )