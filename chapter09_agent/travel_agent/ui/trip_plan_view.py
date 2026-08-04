import pandas as pd
import streamlit as st

def show_trip_plan(trip_plan):
    # 출장 계획 출력 담당
    if not trip_plan.destination:
        return

    trip_df = pd.DataFrame(
        {
            "항목": [
                "출발지",
                "도착지",
                "출장 시작일",
                "출장 종료일",
                "출장 기간",
                "항공편 예약",
                "호텔 예약",
                "날씨 조사"
            ],

            "내용": [
                trip_plan.departure,
                trip_plan.destination,
                trip_plan.start_date,
                trip_plan.end_date,
                trip_plan.period,

                "예"
                if trip_plan.need_flight
                else "아니요",

                "예"
                if trip_plan.need_hotel
                else "아니요",

                "예"
                if trip_plan.need_weather
                else "아니요"
            ]
        }
    )

    st.subheader("📋 출장 계획")

    st.table(trip_df)


    st.markdown(
        "### 출장 계획 요약"
    )

    st.info(
        trip_plan.summary
    )