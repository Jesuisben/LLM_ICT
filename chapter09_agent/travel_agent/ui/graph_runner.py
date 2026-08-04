import streamlit as st

from langchain_core.messages import HumanMessage

from chapter09_agent.travel_agent.utils.file_utils import save_state


# ------------------------------------------------
# LangGraph 실행
# ------------------------------------------------

def run_graph(
    graph,
    state,
    trip_plan
):

    state["trip_plan"] = trip_plan

    state["messages"].append(
        HumanMessage(
            content="출장 계획을 생성해 주세요."
        )
    )

    placeholder = st.empty()

    for event in graph.stream(state):

        node = next(
            iter(event.keys())
        )

        placeholder.info(
            f"🤖 {node.upper()} 실행 중..."
        )

        state.update(
            event[node]
        )

    placeholder.success(
        "✅ 출장 계획 생성 완료"
    )

    st.session_state.state = state

    save_state(state)