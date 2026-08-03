# 그래프 구조 정의
from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from chapter08_langgraph.flow_control.state import State
from chapter08_langgraph.flow_control.nodes import (
    login, search_product, payment, recommend, logout
)
from chapter08_langgraph.flow_control.routers import (
    cart_router, login_router
)


def create_graph():
    graph = StateGraph(State)

    # 노드 추가
    graph.add_node("login", login)
    graph.add_node("search", search_product)
    graph.add_node("payment", payment)
    graph.add_node("recommend", recommend)
    graph.add_node("logout", logout)

    graph.add_edge(START, "login")

    # conditional은 조건식이라는 뜻 (if문 같은)
    graph.add_conditional_edges(
        "login",
        login_router,
        {
            "success": "search",
            "fail": "logout",
        },
    )

    graph.add_conditional_edges(
        "search",
        cart_router,
        {
            "payment": "payment",
            "recommend": "recommend",
        },
    )

    graph.add_edge("payment", "logout")
    graph.add_edge("recommend", "logout")

    graph.add_edge("logout", END)

    return graph.compile()