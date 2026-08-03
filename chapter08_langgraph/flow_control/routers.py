# 분기 조건 관리
from chapter08_langgraph.flow_control.state import State


def login_router(state: State):
    if state["login_success"]:
        return "success"
    else:
        return "fail"


def cart_router(state: State):
    if state["has_cart"]:
        return "payment"
    else:
        return "recommend"