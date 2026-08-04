import streamlit as st


def show_flights(flight_list):
    # 항공편 콤보 박스 담당
    if not flight_list:
        print('항공편 목록 없음')
        return


    st.subheader(
        "✈️ 항공편 선택"
    )


    def flight_label(flight):

        return (
            f"{flight.airline} "
            f"{flight.flight_number}"
        )


    selected_flight = st.selectbox(

        "항공편을 선택하세요",

        flight_list,

        format_func=flight_label
    )


    st.subheader(
        "선택한 항공편 정보"
    )


    st.text(
        str(selected_flight)
    )

    print(selected_flight)
    return selected_flight