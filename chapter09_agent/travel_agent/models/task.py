from enum import Enum
# from typing import Literal
from pydantic import BaseModel, Field

'''
Task 클래스
LLM이 수행해야 할 작업을 하나씩 관리하는 "작업(Task) 객체"입니다.
여행 계획을 세우는 과정에서 각 에이전트에게 어떤 일을 시킬지 기록하고, 완료 여부를 관리하는 역할을 합니다.
'''


class AgentType(str, Enum):
    PLANNER = "planner"
    RESEARCH = "research"
    EXECUTOR = "executor"
    COMMUNICATOR = "communicator"

class Task(BaseModel):
    # 실행할 에이전트 종류를 제한 (4가지 중 하나만 허용)
    agent: AgentType = Field(...)
    # Pydantic 내부에서 Field(...)는 '이 필드는 Required'라는 의미입니다.

    # 작업 완료 여부
    done: bool = False

    # 작업 설명 (슈퍼바이저가 생성하는 task 내용)
    description: str

    # 작업 완료 시간 (문자열로 저장)
    done_at: str = ""

    # Task 객체를 dict 형태로 변환 (저장/직렬화용)
    def to_dict(self):
        return {
            "agent": self.agent,
            "done": self.done,
            "description": self.description,
            "done_at": self.done_at
        }
# end class Task