# ============================================================
# DuckDuckGo 검색과 관련한 모듈 파일입니다.
# ============================================================
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# ============================================================
# Constant
# ============================================================
DOCUMENT_SEPARATOR = "\n\n"
# ============================================================
# DuckDuckGo 뉴스 검색
# ============================================================
def search_news(
    # question : 질문, region="kr-ko" : 지역, time="w" : 검색 기간을 의미 (w:week)
    question,
    region="kr-ko",
    time="w",
):
    engine = create_news_engine(region, time)

    return engine.invoke(question)

# ============================================================
# 뉴스 검색 엔진 생성
# ============================================================
def create_news_engine(
    region="kr-ko",
    time="w",
):
    # 해당 지역과 검색 기간을 사용하여 Wrapper 객체를 생성합니다.
    wrapper = DuckDuckGoSearchAPIWrapper(
        region=region,
        time=time
    )

    # 뉴스들을 검색하되, 구분자로 엔터 키 2번으로 구분합니다.
    return DuckDuckGoSearchResults(
        api_wrapper=wrapper,
        source="news",
        # results_separator : 여러 검색 결과를 하나의 문자열로 합칠 때 사용하는 구분자 (기본 값은 ", ")
        results_separator=DOCUMENT_SEPARATOR
    )

# ============================================================
# 일반 검색을 위한 DuckDuckGo 검색 엔진 생성
# ============================================================
def search(question):
    engine = DuckDuckGoSearchResults(
        results_separator=DOCUMENT_SEPARATOR
    )

    return engine.invoke(question)

# ============================================================
# 검색된 결과물에서 URL을 추출합니다.
# ============================================================
def extract_links(documents):
    links = []

    # 빈 내용물이 들어오면 마찬가지로 빈 값을 반환함
    if documents is None:
        return links

    for doc in documents.split(DOCUMENT_SEPARATOR):
        try:
            if "link:" not in doc:
                continue # 현재 문서 doc에는 "link:"가 없구나
            url_link = doc.split("link:")[1].strip()
            links.append(url_link)

        except Exception as err:
            print(err)
            continue

    return links