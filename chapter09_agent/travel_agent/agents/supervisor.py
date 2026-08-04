from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from chapter09_agent.travel_agent.state import State
from chapter09_agent.travel_agent.models.task import Task

# [출력 형식]
#             반드시 JSON 형태로 출력한다.
#
#             {{
#               "agent": "planner | research | executor | communicator",
#               "description": "왜 이 에이전트를 선택했는지 간단한 이유"
#             }}

# 출장 준비를 제공해주는 AI 시스템의 Supervisor(관리자) 클래스입니다.
def supervisor(state: State, model):
    prompt = PromptTemplate.from_template(
        """
            너는 출장 준비 AI 시스템의 Supervisor(관리자)야.
            사용자의 대화를 분석하여 다음 에이전트 중 하나를 반드시 선택해줘.

            [선택 가능한 에이전트]
            - planner: 출장 계획 수립(목적지, 기간 등 결정)
            - research: 항공권/호텔/날씨 정보 조사
            - executor: 최종 보고서 생성
            - communicator: 최종 결과 사용자 전달

            [현재 상태]
            - messages: {messages}
            - task_history: {task_history}

            [규칙]
            1. 반드시 하나의 agent만 선택한다.
            2. 이전 task_history를 참고하여 순차적으로 진행한다.
            3. 이미 planner가 끝났다면 research로 넘어간다.
            4. research가 끝났다면 executor로 간다.
            5. executor 이후에는 communicator로 간다.
            6. 사용자가 새로운 요청을 하면 다시 planner로 시작할 수 있다.            
        """
    )

    chain = prompt | model.with_structured_output(Task)

    task = chain.invoke(
        {
            "messages": state["messages"],
            "task_history": state["task_history"]
        }
    )

    state["task_history"].append(task)

    state["messages"].append(
        AIMessage(f"[Supervisor] {task}")
    )

    return state
# end def supervisor

def supervisor_router(state: State):
    task = state["task_history"][-1]

    return task.agent