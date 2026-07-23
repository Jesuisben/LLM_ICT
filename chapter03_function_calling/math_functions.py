def calculate(operation: str, a: float, b: float):
    # "사칙연산을 수행하는 함수
    if operation == "add":
        result = a + b
    elif operation == "sub":
        result = a - b
    elif operation == "mul":
        result = a * b
    elif operation == "div":
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return "Error: Unknown operation"

    return f"Result: {result}"

# tools는 LLM에게 '이러한 함수가 존재함'을 알려 주는 함수 명세서(JSON 계약서) 역할을 합니다.
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "두 숫자에 대해 사칙연산을 수행합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "연산 종류 (add, sub, mul, div)"
                    },
                    "a": {
                        "type": "number",
                        "description": "첫 번째 숫자"
                    },
                    "b": {
                        "type": "number",
                        "description": "두 번째 숫자"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        }
    }
]
