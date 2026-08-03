# 각 노드의 비즈니즈 로직 담당
# state.py에서 지정한 State의 양식을 가져옴
from chapter08_langgraph.flow_control.state import State

# 로그인을 수행할 때 수행이 되는 Node
def login(state: State):
    state["logs"].append("🔑 로그인")
    return state


def search_product(state: State):
    state["logs"].append("🛒 상품 조회")
    return state


def payment(state: State):
    state["logs"].append("💳 결제 진행")
    return state


def recommend(state: State):
    state["logs"].append("🎁 상품 추천")
    return state


def logout(state: State):
    state["logs"].append("✅ 로그 아웃")
    return state