# from openai import OpenAI
# client = OpenAI(api_key=api_key)
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from utility.env_util import get_api_key

from typing import Literal
from pydantic import BaseModel, Field

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
# print(api_key)

model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0.3,
    max_completion_tokens=100
)


messages = [
    # 원래의 system
    SystemMessage(content="너는 카페에서 일하는 직원이다. 손님에게 짧고 친절하게 응대해줘."),
    # 원래의 user
    HumanMessage(content="안녕하세요. 케이크랑 음료 추천해 주세요.")
]
print("# StrOutputParser를 적용하기 이전")
print(model.invoke(messages))

parser = StrOutputParser()
result = model.invoke(messages)
print("\n# StrOutputParser를 적용하기 이후")
print(parser.invoke(result))

# LCEL Chain 구성
chain = model | parser
print(chain.invoke(messages))

system_template = "너는 {place}에서 일하는 {role}이다. 손님에게 짧고 친절하게 대답해줘"
human_template = "{menu} 추천해주세요"

prompt_template =  ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", human_template)
])

chain = prompt_template | model | parser
response = chain.invoke({
    "place":"카페", "role":"직원", "menu":"케이크랑 음료"
})
print(response)

inputs = [
    {"place":"카페", "role":"직원", "menu":"음료"},
    {"place":"중국집", "role":"직원", "menu":"음식"}
]

print("배치 처리")
# 원래 invoke()를 자주 쓰지만
# 여러개를 한번에 처리할때는 batch를 사용함
results = chain.batch(inputs)

for input_data, result in zip(inputs, results):
    print(f"# 입력값 : {input_data}")
    print(f"# 결과   : {result}")
    print("-" * 30)

class CafeResponse(BaseModel):
    answer: str = Field(description="카페 직원의 응답 (짧게)")
    emotion: Literal["친절", "중립"] = Field(description="응답의 분위기")

# "AI야, 너의 답변은 반드시 CafeResponse 구조로 만들어야 되."
#----------------------------------------------------------
# 단계10. Structured Output Chain 구성
#----------------------------------------------------------
parser_condition = model.with_structured_output(CafeResponse)

new_chain = prompt_template | parser_condition

response = new_chain.invoke({
    "place": "카페",
    "role": "직원",
    "menu": "초코 케이크랑 커피",
})
print(response)