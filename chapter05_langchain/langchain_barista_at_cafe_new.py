# from openai import OpenAI
# # 그냥 openai로는 langchain을 사용할 수 없음
# client = OpenAI(api_key=api_key)

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# 변수 하나하나를 Field라고 부름
from pydantic import BaseModel, Field

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

# 1. 모델 생성
model = ChatOpenAI(
    model='gpt-4o',
    temperature=0.3,
    max_completion_tokens=150
)

# 3. PromptTemplate 생성
# ChatPromptTemplate.from_messages( [ ("역할", "내용"), ("역할", "내용") ] )
# 특정 부분만 바뀌고 반복하는 문장을 효율적으로 사용하기 위해
# 바뀌는 특정부분만 교체해서 문장을 만들기
# ex) 너는 {who}야.. 따뜻한 {what} 알려줘
# 각 요소는 튜플임.
# ChatPromptTemplate.from_messages()가 이 형식을 알고 있어서 첫 번째 위치는 역할, 두 번째 위치는 내용으로 해석함
# 따라서 굳이 사전으로 작성하지 않아도 알아서 서로의 키와 값?을 매핑함
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "{system_role}"),
    ("user", "{question}")
])

# 2. OutputParser 출력 파서 생성
str_parser = StrOutputParser()


# 4. 체인 생성 (1, 2, 3을 묶어줌)
# (적을 순서 : 3 -> 1 -> 2) (구분자 : |)
str_chain = (prompt_template | model | str_parser)

# ============================================================
# 역할(Role) 정의
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
# 사용자 질문 정의
# ============================================================
question_dict = {
    "바리스타":
        "오늘 너무 피곤한데 어떤 커피가 좋을까?",

    "한의사":
        "요즘 너무 피곤하고 기운이 없는데 어떻게 해야 할까?"
}

# ============================================================
# JSON 출력 모델
# ============================================================
# Pydantic이 나오면 보통 Advice() 클래스를 사용한다고 생각하면 됨
# 그렇게 국룰로 클래스 이름을 Advice로 정한것이지 강제는 아님
# 꼭!! BaseModel은 pydantic 모델을 사용해야 함
# Pydantic의 BaseModel 클래스를 상속받음
class Advice(BaseModel):
    # Field()를 꼭 pydantic.fields로 가져오기
    # recommendation, reason, method는 모두 클래스의 필드(field)
    # : str은 해당 필드에 들어갈 데이터 타입 (일반적으로 파이썬은 타입을 지정할 수 없지만 pydantic은 가능함)
    recommendation : str = Field(description="추천 또는 조언")
    reason : str = Field(description="추천 이유")
    method : str = Field(description="실천 방법")

# Json으로 출력하는 JsonOutputParser의 매개변수에 pydantic의 변수를 생성했던 class를 넣음
json_parser = JsonOutputParser(pydantic_object=Advice)

# OutputParser 출력 파서 생성
# str체인과 똑같은 표현식인데 parser만 바꿈 ( 표현식 : ( prompt_template | model | json_parser ) )
json_chain = ( prompt_template | model | json_parser )


# 역할별 반복 실행
for role in system_roles:
    your_role = role["your_role"]
    system_prompt = role["content"]
    # dict.get(키, 기본값) : 사용하는 이유 - 그냥 []을 이용해서 값을 가져오면 키가 없을때 오류가 발생함
    # get()은 기본값을 설정할 수 있어서 오류를 방지하기 위해 사용함
    question = question_dict.get(your_role, "좋은 조언을 해주세요.")

    print("*" * 50)
    print(f"현재 역할 : {your_role}")
    print(f"질문 내용 : {question}")
    print(f"시스템 프롬프트 : {system_prompt}")

    print("# StrOutputParser 실행 결과")
    # chain의 메소드는 invoke()를 제일 많이 씀 (암기하기)
    # invoke()할때 매개변수들을 치환함
    # PromptTemplate에는 {}를 넣지만 invoke()에는 {}를 넣으면 안됨
    str_result = str_chain.invoke({
        "system_role":your_role,
        "question":question
    })

    print(str_result)

    print("\n# JsonOutputParser 실행 결과")

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

    print(f"추천 : {json_result['recommendation']}")
    print(f"이유 : {json_result['reason']}")
    print(f"방법 : {json_result['method']}")

# end for