import streamlit as st

from chapter09_agent.travel_agent.ui.trip_plan_view import show_trip_plan
from chapter09_agent.travel_agent.ui.flight_view import show_flights
from chapter09_agent.travel_agent.ui.hotel_view import show_hotel
from chapter09_agent.travel_agent.ui.weather_view import show_weather


# ------------------------------------------------
# 결과 출력
# ------------------------------------------------
def show_result(
    state
):

    show_trip_plan(
        state["trip_plan"]
    )

    research = state[
        "research_result"
    ]

    show_flights(
        research.flight_list
    )

    show_hotel(
        research.hotel_list
    )

    show_weather(
        research.weather
    )

    if state["final_report"]:

        st.subheader(
            "최종 보고서"
        )

        st.markdown(
            state["final_report"]
        )