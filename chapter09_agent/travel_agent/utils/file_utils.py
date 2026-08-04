import json
import os

from datetime import datetime
from pydantic import BaseModel


def to_json_data(obj):
    """
    Pydantic 객체를 JSON 저장 가능한 형태로 변환
    """

    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")

    if isinstance(obj, list):
        return [to_json_data(item) for item in obj]

    if isinstance(obj, dict):
        return {
            key: to_json_data(value)
            for key, value in obj.items()
        }

    return obj


def save_state(state):

    os.makedirs(
        "data",
        exist_ok=True
    )

    filename = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    state_dict = {

        "messages": [
            {
                "type": message.__class__.__name__,
                "content": message.content
            }
            for message in state["messages"]
        ],

        "task_history": [
            task.to_dict()
            for task in state["task_history"]
        ],

        "trip_plan": to_json_data(
            state["trip_plan"]
        ),

        "research_result": to_json_data(
            state["research_result"]
        ),

        "final_report": state["final_report"]
    }

    filepath = os.path.join(
        "data",
        f"{filename}.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state_dict,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"저장 완료 : {filepath}")