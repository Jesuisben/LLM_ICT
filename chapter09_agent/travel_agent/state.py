from typing import TypedDict, List
from langchain_core.messages import AnyMessage
from chapter09_agent.travel_agent.models.task import Task
from chapter09_agent.travel_agent.models.trip_plan import TripPlan
from chapter09_agent.travel_agent.models.research_result import ResearchResult
from chapter09_agent.travel_agent.models.execution_result import ExecutionResult

# TypedDict
# 일반적인 딕셔너리는 아무 키나 넣을 수 있습니다.
# TypedDict를 사용하면 어떤 키가 있어야 하고, 각 키의 값이 어떤 타입인지를 정의할 수 있습니다.
# List는 리스트 안에 어떤 타입의 데이터가 들어가는지를 한정하기 위하여 사용하나 클래스입니다.

class State(TypedDict):
    # 대화 메시지 기록 (user / AI / system 메시지 전체)
    messages: List[AnyMessage]

    # 에이전트 실행 이력 (planner, research 등 task 단위 기록)
    task_history: List[Task]

    # 출장 계획 정보 (목적지, 기간, 필요 여부 등)
    # trip_plan: dict
    trip_plan: TripPlan

    # 조사 결과 (항공, 호텔, 날씨 정보)
    research_result: ResearchResult # 이 항목도 TripPlan 형식으로 만들기

    execution_result: ExecutionResult

    # 최종 생성된 보고서
    final_report: str

# end class State