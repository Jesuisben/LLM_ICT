import streamlit as st

from datetime import (
    date,
    timedelta
)

from chapter09_agent.travel_agent.models.trip_plan import TripPlan

from chapter09_agent.travel_agent.constant.constants  import AIRPORTS


# ------------------------------------------------
# 출장 정보 입력
# ------------------------------------------------

def input_trip():

    # --------------------------------------------
    # 1행 : 출발 공항 / 도착 공항
    # --------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        departure = st.selectbox(
            "출발 공항",
            AIRPORTS
        )

    with col2:
        destination = st.selectbox(
            "도착 공항",
            AIRPORTS,
            index=3
        )

    # --------------------------------------------
    # 2행 : 출장 시작일 / 출장 종료일
    # --------------------------------------------

    today = date.today()

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "출장 시작일",
            min_value=today
        )

    with col2:

        end_date = st.date_input(
            "출장 종료일",
            min_value=today + timedelta(days=3)
        )

    # --------------------------------------------
    # 3행 : 예약/조회 옵션
    # --------------------------------------------

    col1, col2, col3, col4 = st.columns([2, 2, 2, 6])

    with col1:

        need_flight  = st.checkbox(
            "항공편 예약",
            value=True
        )

    with col2:

        need_hotel  = st.checkbox(
            "호텔 예약",
            value=True
        )

    with col3:

        need_weather  = st.checkbox(
            "도착지 날씨",
            value=True
        )

    # --------------------------------------------
    # TripPlan 생성
    # --------------------------------------------

    return TripPlan(
        departure=departure,
        destination=destination,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        period=f"{start_date} ~ {end_date}",
        need_flight =need_flight ,
        need_hotel =need_hotel ,
        need_weather =need_weather
    )