"""
LangChain PromptTemplate + OutputParser + Role 반복 처리 예제

설치:
pip install langchain langchain-openai python-dotenv
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser
)

from utility.env_util import get_api_key

# ============================================================
# 1. OpenAI API Key 설정
# ============================================================
find_api = "OPENAI_API_KEY"

api_key = get_api_key(find_api)
# ============================================================
# 2. LLM Model 객체 생성
# ============================================================
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_completion_tokens=150,
)
# ============================================================
# 3. 역할(Role) 정의
# ============================================================
system_roles = [
    {
        "your_role": "바리스타",
        "content":
            """
            너는 커피 전문점의 바리스타야.
            항상 친절하고 메뉴를 추천해주는 말투로 답변해.
            """
    },
    {
        "your_role": "한의사",
        "content":
            """
            너는 한의학에 정통한 전통 한의사다.
            몸의 기운과 컨디션을 고려하여
            차분하고 조언하듯 답변해라.
            """
    }
]
# ============================================================
# 4. 사용자 질문 정의
# ============================================================
question_dict = {
    "바리스타":
        "오늘 너무 피곤한데 어떤 커피가 좋을까?",

    "한의사":
        "요즘 너무 피곤하고 기운이 없는데 어떻게 해야 할까?"
}
# ============================================================
# 5. Prompt Template 생성
# ============================================================
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "{system_role}"
        ),

        (
            "user",
            "{question}"
        )
    ]
)
# ============================================================
# 6. StrOutputParser Chain 생성
# ============================================================
str_parser = StrOutputParser()

str_chain = (
    prompt_template
    | model
    | str_parser
)
# ============================================================
# JSON 출력 모델
# ============================================================
class Advice(BaseModel):
    recommendation: str = Field(description="추천 또는 조언")
    reason: str = Field(description="추천 이유")
    method: str = Field(description="실천 방법")

# ============================================================
# 7. JsonOutputParser Chain 생성
# ============================================================
json_parser = JsonOutputParser(pydantic_object=Advice)


json_chain = (
    prompt_template
    | model
    | json_parser
)
# ============================================================
# 8. 역할별 반복 실행
# ============================================================
for role in system_roles:
    your_role = role["your_role"]

    system_prompt = role["content"]

    question = question_dict.get(
        your_role,
        "좋은 조언을 해주세요."
    )

    print()
    print("=" * 70)
    print(f"현재 역할 : {your_role}")
    print(f"질문 내용 : {question}")
    print("=" * 70)
    # --------------------------------------------------------
    # 8-1. StrOutputParser 결과
    # --------------------------------------------------------
    print("[ StrOutputParser 결과 ]")
    print("-" * 70)

    str_result = str_chain.invoke(
        {
            "system_role":
                system_prompt,

            "question":
                question
        }
    )

    print(str_result)
    # --------------------------------------------------------
    # 8-2. ListOutputParser 결과
    # --------------------------------------------------------
    print("[ ListOutputParser 결과 ]")
    print("-" * 70)

    json_result = json_chain.invoke(
        {
            "system_role": system_prompt,

            "question":
                f"""
    {question}

    다음 형식의 JSON으로만 답변하세요.

    {json_parser.get_format_instructions()}
    """
        }
    )

    print("\n[ JsonOutputParser 결과 ]")
    print("-" * 70)

    print(f"추천 : {json_result['recommendation']}")
    print(f"이유 : {json_result['reason']}")
    print(f"방법 : {json_result['method']}")

print()
print("=" * 70)
print("모든 역할 처리 완료")
print("=" * 70)