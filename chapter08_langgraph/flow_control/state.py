# 상태 관리자 : LangGraph 전반에 걸쳐 있는 State를 관리해주는 파일
# 상태를 관리해주는 파일
from typing import TypedDict

# node들이 관리하려는 데이터들 정리
class State(TypedDict):
    login_success: bool # 로그인 여부
    has_cart: bool # 장바구니에 상품 존재 여부
    logs: list[str] # 작업 히스토리를 저장하는 리스트