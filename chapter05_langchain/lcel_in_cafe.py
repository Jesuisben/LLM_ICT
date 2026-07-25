import os, sys

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from pydantic import BaseModel, Field
#----------------------------------------------------------
# 단계01. 환경 설정
#----------------------------------------------------------
project_root = os.path.dirname(os.getcwd())
print(f'project_root : {project_root}')
sys.path.insert(0, project_root)

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)
#----------------------------------------------------------
# 단계02. ChatOpenAI 모델 생성
#----------------------------------------------------------
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,  # 말이 길어지는 걸 방지
    max_completion_tokens=100,    # 응답 최대 길이 제한, 최신 버전에는 max_tokens 대신 사용 
)
#----------------------------------------------------------
# 단계03. Message 기반 LLM 호출(카페 역할극)
#----------------------------------------------------------
messages = [
    SystemMessage(content="너는 카페에서 일하는 직원이다. 손님에게 짧고 친절하게 응대해줘."),
    HumanMessage(content="안녕하세요. 케이크랑 음료 추천해 주세요."),
]
print('# StrOutputParser를 적용하기 이전입니다.')
model.invoke(messages)
#----------------------------------------------------------
# 단계04. StrOutputParser 적용
# 인보크한 모델을 출력 parser에게 다시 인보크시켜서 필요한 문자열만 출력해 줍니다.
#----------------------------------------------------------
parser = StrOutputParser()

result = model.invoke(messages)
print('# StrOutputParser를 적용시킨 결과입니다.')
parser.invoke(result)
#----------------------------------------------------------
# 단계05. LCEL Chain 구성
# 파이프(|) 연산자는 Runnable 합성 연산자라고 하며, 왼쪽의 출력 정보를 오른쪽의 입력 정보로 입력하는 역할을 합니다.
#----------------------------------------------------------
chain = model | parser
chain.invoke(messages)
#----------------------------------------------------------
# 단계06. Prompt Template 생성 : ChatPromptTemplate로 카페 상황 일반화
#----------------------------------------------------------
system_template = "너는 {place}에서 일하는 {role}이다. 손님에게 짧고 친절하게 대답해줘."
human_template = "{menu} 추천해 주세요."

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", human_template),
])
#----------------------------------------------------------
# 단계07. Prompt + Model + Parser (LCEL) Chain 구성
#----------------------------------------------------------
chain = prompt_template | model | parser

chain.invoke({
    "place": "카페",
    "role": "직원",
    "menu": "케이크랑 음료",
})
#----------------------------------------------------------
# 단계08. Batch 처리
#----------------------------------------------------------
print('# 여러 개의 입력은 batch 처리(한 번에 처리)를 사용하면 좋습니다.')
inputs = [
    {"place": "카페", "role": "직원", "menu": "음료"},
    {"place": "카페", "role": "직원", "menu": "빵"},
]

results = chain.batch(inputs)

for input_data, result in zip(inputs, results):
    print(f"# 입력값 : {input_data}")
    print(f"# 결과   : {result}")
    print("-" * 30)
#----------------------------------------------------------
# 단계09. Pydantic 출력 모델 정의
# 반드시 { answer: 문자열, emotion: '친절' 또는 '중립' }의 구조로 대답해 줘야되.
# with_structured_output() : 출력 형식은 반드시 CafeResponse 스키마를 따라서 처리해야 합니다.(출력 형식 강제 지정)
#----------------------------------------------------------
class CafeResponse(BaseModel):
    answer: str = Field(description="카페 직원의 응답 (짧게)")
    emotion: Literal["친절", "중립"] = Field(description="응답의 분위기")

# "AI야, 너의 답변은 반드시 CafeResponse 구조로 만들어야 되."
#----------------------------------------------------------
# 단계10. Structured Output Chain 구성
#----------------------------------------------------------
parser_condition = model.with_structured_output(CafeResponse)

new_chain = prompt_template | parser_condition

new_chain.invoke({
    "place": "카페",
    "role": "직원",
    "menu": "초코 케이크랑 커피",
})
#----------------------------------------------------------