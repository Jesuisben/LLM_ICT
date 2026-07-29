# pip install -U ddgs
# pip install -U duckduckgo-search
# duckduckgo-search는 DuckDuckGo 검색을 파이썬에서 사용하기 위한 비공식 라이브러리의 예전 패키지명입니다.
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import os, sys, requests
from bs4 import BeautifulSoup

# USER_AGENT 설정
os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# DuckDuckGo API wrapper를 사용하여 검색할 때 검색 매개변수를 설정하기 위한 클래스 import
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from langchain_community.document_loaders import WebBaseLoader

project_root = os.path.dirname(os.getcwd())
sys.path.insert(0, project_root)

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

question = '최근 MZ세대의 주요 소비 트렌드는 무엇인가요?'  # 질문 내용

# max_completion_tokens 항목을 사용하여 출력 토큰의 수를 조정하도록 합니다.
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0.3,
    max_completion_tokens=100,
)

# response = model.invoke(question)
# print('\nresponse')
# print(response)
#
# print('\nresponse.content')
# print(response.content)

# DuckDuckGoSearchResults 클래스의 반환 값은 LangChain의 Document 객체가 아니라 문자열(str)입니다.
ddg_engine = DuckDuckGoSearchResults(results_separator='\n\n')
docs = ddg_engine.invoke(question)

print(f'type(docs) = {type(docs)}')
print("\nStart of docs output")
print('='*50)
print(docs)
print('='*50)
print("End of docs output")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "사용자의 질문에 대해 아래 context에 기반하여 답변해줘.:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model

# 채팅 메시지를 저장할 메모리 객체 생성
chat_history = InMemoryChatMessageHistory()

# 사용자 질문을 메모리에 저장
chat_history.add_user_message(question)

# 문서 검색하고 답변 생성
answer = chain.invoke(
    {
        "messages": chat_history.messages,
        "context": docs,
    }
)

# 생성된 답변을 메모리에 저장
chat_history.add_ai_message(answer)

print('\nanswer')
print(answer)

# 한국 지역("kr-kr")을 기준, 최근 일주일("w") 내의 검색 결과를 가져오도록 초기화
wrapper = DuckDuckGoSearchAPIWrapper(region="kr-ko", time="w")

# 검색 기능을 위한 DuckDuckGoSearchResults 초기화
ddg_engine = DuckDuckGoSearchResults(
    api_wrapper=wrapper,      # 앞에서 정의한 API wrapper를 사용
    source="news",            # 뉴스 소스에서만 검색하도록 지정
    results_separator='\n\n'   # 결과 항목 사이의 구분자(줄바꿈 2개)
)

# 검색 키워드 question에 대하여 검색하고 해당 결과를 docs에 저장합니다.
docs = ddg_engine.invoke(question)

# 검색 결과 출력
print('\ndocs')
print(docs)

# naver는 외부 검색 엔진을 대부분 차단합니다.
# ytn.co.kr은 DuckDuckGo를 사용한 크롤링을 허용합니다.
# DuckDuckGo를 이용해 ytn.co.kr 사이트에서 검색어 question에 대한 내용을 검색
# "site:"는 대부분의 검색 엔진에서 제공하는 검색 연산자(Search Operator) 입니다.
docs = ddg_engine.invoke("site:ytn.co.kr " + question)
print('\nsite:ytn.co.kr---docs')
print(docs)

# 웹페이지 내용 가져오기
# 검색 결과의 링크들을 저장할 빈 리스트 초기화
link_list = []

# 검색 결과를 줄바꿈 기준으로 분리하고, 각 결과 항목에서 링크를 추출
for doc in docs.split("\n\n"):
    print('\none document')
    print(doc)  # 각 검색 결과 항목을 출력하여 확인
    link = doc.split("link:")[1].strip()  # 각 항목에서 'link:' 이후의 URL 부분만 추출
    link_list.append(link)  # 추출한 링크를 리스트에 추가

# 모든 링크를 출력
print('\nlink_list')
print(link_list)

# Langchain의 WebBaseLoader를 사용하여 웹 페이지의 내용을 불러옵니다.
# WebBaseLoader 객체를 생성. 'link_list'는 웹 페이지의 URL 목록을 담고 있는 변수
# bs_get_text_kwargs는 BeautifulSoup의 get_text() 메소드에 전달될 추가 인자
loader = WebBaseLoader(
    web_paths=link_list,  # 웹 페이지의 링크 목록을 지정
    bs_get_text_kwargs={
        "strip": True  # 웹 페이지에서 텍스트를 가져올 때 앞뒤의 공백을 제거
    },
)

# 비동기로 웹 페이지의 내용을 로드하고, 각 문서를 page_contents 리스트에 추가
page_contents = []  # 각 웹 페이지의 내용을 저장할 리스트입니다.
async for doc in loader.alazy_load():
    page_contents.append(doc)  # 불러온 문서를 page_contents 리스트에 추가

print('\nWebBaseLoader로 웹 페이지 내용 읽기')
# page_contents에 있는 각 웹 페이지의 내용을 출력
for content in page_contents:
    # print(content[0:100])  # 웹 페이지의 내용을 출력(너무 길어서 글자 일부만 출력)
    print(content.page_content[0:300])
    print('-' * 40)

# 주어진 URL에서 기사 텍스트를 가져 오는 함수
def get_article_text(url):
    try:
        # URL에 GET 요청을 보냄
        response = requests.get(url)
        # 요청이 성공하지 못하면 예외를 발생시킴
        response.raise_for_status()

        # BeautifulSoup을 사용하여 HTML 내용을 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 클래스가 'story-news article'인 <article> 태그를 찾음
        article = soup.find('article', class_='story-news article')

        # 기사를 찾았다면 그 텍스트를 반환
        if article:
            return article.get_text(strip=True)
        else:
            try:
                if soup.find('article'):
                    return soup.find('article').get_text(strip=True)
                elif soup.find('div', id="CmAdContent"):
                    return soup.find('div', id="CmAdContent").get_text(strip=True)
            except:
                return "기사 내용을 찾을 수 없습니다."

    # 요청이 실패할 경우 예외 처리
    except requests.exceptions.RequestException as e:
        return f"URL을 가져오는 중 오류 발생: {e}"

print('URL 목록의 각 링크를 반복하면서 기사 텍스트를 출력')
articles = []    # 가져온 내용을 리스트에 담기 위한 변수 선언

for link in link_list:
    print(f"URL: {link}\n")
    article_text = get_article_text(link)
    print(f"Content:\n{article_text}")
    print("-"*40)
    articles.append(article_text)

# None 제거 후 join
clean_articles = [a for a in articles if a is not None]
chat_history.add_message("\n".join(clean_articles))

chat_history.add_user_message(question)

# 문서 검색하고 답변을 생성
answer = chain.invoke(
    {
        "messages": chat_history.messages,
        "context": docs,
    }
)

print('# 원본 질문 내용')
print(question)

print('\n# 생성된 답변 메모리에 저장')
chat_history.add_ai_message(answer)
# print(answer)

# 출력
print("=" * 80)
print("# 사용자 질문")
print("=" * 80)
print(question)

print("\n" + "=" * 80)
print("# AI 생성 답변")
print("=" * 80)
print(answer.content)

print("\n" + "=" * 80)
print("# 토큰 사용량")
print("=" * 80)

usage = answer.response_metadata["token_usage"]

print(f"입력 토큰 : {usage['prompt_tokens']}")
print(f"출력 토큰 : {usage['completion_tokens']}")
print(f"전체 토큰 : {usage['total_tokens']}")