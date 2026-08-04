from datetime import datetime
import sys

from langchain_core.prompts import PromptTemplate

from chapter09_agent.travel_agent.state import State
from chapter09_agent.travel_agent.models.trip_plan import TripPlan
from chapter09_agent.travel_agent.utils.logger_util import logger

def planner_agent(state: State, model):
    """출장 계획을 보완하는 Planner Agent"""

    # UI에서 입력한 출장 정보
    current_plan: TripPlan = state["trip_plan"]

    prompt = PromptTemplate.from_template(
        """
당신은 출장 Planner를 위한 AI입니다.

사용자가 이미 다음 정보를 입력하였습니다.

출발지 : {departure}
도착지 : {destination}
출장 시작일 : {start_date}
출장 종료일 : {end_date}
항공편 예약 여부 : {need_flight}
호텔 예약 여부 : {need_hotel}
도착지 날씨 확인 여부 : {need_weather}

위의 정보는 절대로 변경하지 않도록 합니다.

다음 항목만 판단하여 작성하되, 응답의 모든 문자열은 반드시 한국어를 사용하도록 합니다.

- summary

반드시 TripPlan 객체 형식으로 반환해 주도록 합니다.
"""
    )

    # LLM의 결과를 TripPlan 객체로 바로 반환
    structured_model = model.with_structured_output(TripPlan)

    chain = prompt | structured_model

    try:

        result: TripPlan = chain.invoke(
            {
                "departure": current_plan.departure,
                "destination": current_plan.destination,
                "start_date": current_plan.start_date,
                "end_date": current_plan.end_date,
                "need_flight": current_plan.need_flight,
                "need_hotel": current_plan.need_hotel,
                "need_weather": current_plan.need_weather
            }
        )

        #
        # LLM이 변경하면 안 되는 값은 기존 값을 그대로 유지
        #
        result.departure = current_plan.departure
        result.destination = current_plan.destination
        result.start_date = current_plan.start_date
        result.end_date = current_plan.end_date
        result.period = current_plan.period

        state["trip_plan"] = result

        print("\n===== planner_agent =====")
        print(type(result))
        print(result)

    except Exception as err:

        # print("\n===== planner_agent ERROR =====")
        # print(err)
        logger.error(
            "===== planner_agent ERROR ====="
        )

        logger.exception(err)

        # 실패하면 기존 TripPlan 그대로 사용
        state["trip_plan"] = current_plan

    # 작업 완료 처리
    task = state["task_history"][-1]
    task.done = True
    task.done_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return state
