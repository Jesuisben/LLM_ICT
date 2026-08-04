from datetime import datetime

from langchain_core.messages import AIMessage

from chapter09_agent.travel_agent.state import State


def communicator_agent(
        state: State,
        model
):

    print("\n===== COMMUNICATOR =====")

    trip = state["trip_plan"]
    result = state["execution_result"]

    # -----------------------------------------
    # Prompt 생성
    # -----------------------------------------

    sections = []

    # -----------------------------------------
    # 출장 계획
    # -----------------------------------------

    sections.append(
        f"""
당신은 출장 비서입니다.

아래 정보를 이용하여 Markdown 형식의 출장 보고서를 작성하세요.

# 출장 계획

출발지 : {trip.departure}

도착지 : {trip.destination}

기간 : {trip.period}
""".strip()
    )

    # -----------------------------------------
    # 항공편
    # -----------------------------------------

    if trip.need_flight and result.flight:

        sections.append(
            f"""
# 항공편

노선 : {result.flight.route}

항공사 : {result.flight.airline}

편명 : {result.flight.flight_number}

가격 : {result.flight_price:,.0f}원
""".strip()
        )

    # -----------------------------------------
    # 호텔
    # -----------------------------------------

    if trip.need_hotel and result.hotel:

        sections.append(
            f"""
# 호텔

호텔명 : {result.hotel.name}

객실 : {result.hotel.room_type}

숙박비 : {result.hotel_price:,.0f}원
""".strip()
        )

    # -----------------------------------------
    # 날씨
    # -----------------------------------------

    if trip.need_weather and result.weather:

        sections.append(
            f"""
# 날씨

날씨 : {result.weather.weather}

기온 : {result.weather.temperature}

습도 : {result.weather.humidity}

강수확률 : {result.weather.rain_probability}
""".strip()
        )

    # -----------------------------------------
    # 총 비용
    # -----------------------------------------

    sections.append(
        f"""
# 총 비용

{result.total_cost:,.0f}원

마지막에는 출장 준비 체크리스트도 작성하세요.
""".strip()
    )

    prompt = "\n\n".join(sections)

    # -----------------------------------------
    # LLM 호출
    # -----------------------------------------

    response = model.invoke(prompt)

    report = response.content

    state["final_report"] = report

    state["messages"].append(
        AIMessage(content=report)
    )

    task = state["task_history"][-1]

    task.done = True

    task.done_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return state