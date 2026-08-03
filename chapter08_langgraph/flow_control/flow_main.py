# 프로그램의 시작점으로, UI와 그래프를 연결합니다.
import sys
import streamlit as st
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chapter08_langgraph.flow_control.graph import create_graph
from chapter08_langgraph.flow_control.ui import draw_ui


graph = create_graph()


def main():

    login_success, has_cart = draw_ui()

    if st.button("실행"):
        # 스테이트 초기 값
        state = {
            "login_success": login_success,
            "has_cart": has_cart,
            "logs": [],
        }

        result = graph.invoke(state)

        st.subheader("실행 순서")

        for log in result["logs"]:
            st.write(log)


if __name__ == "__main__":
    main()