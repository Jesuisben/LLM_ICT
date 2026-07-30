# ============================================================
# 검색된 url 주소를 이용하여 웹 기사 내용을 수집하는 모듈입니다.
# ============================================================
import requests

# BeautifulSoup : 정적인 HTML 문서를 분석하여 원하는 데이터를 추출할 때 사용
# 동적인 페이지를 처리할 때 사용하는 대체 도구 : Selenium
from bs4 import BeautifulSoup

from chapter07_search_engine.duckduckgo.search_util import DOCUMENT_SEPARATOR


# ============================================================
# 여러 url의 기사 정보 읽기
# ============================================================
def get_articles(link_list):
    articles = []

    for link in link_list:
        text = get_article_text(link)
        articles.append(text)

    return articles
# ============================================================
# 1개의 url 주소에서 기사 내용에 대한 본문을 추출합니다.
# ============================================================
# (url: str) -> str
# 매개변수의 타입이 str이고 반환타입도 str이라는 뜻
def get_article_text(url: str) -> str:
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        # 요청이 실패한 경우 예외를 발생시킴
        response.raise_for_status()

        # print("response.content")
        # print(response.content)
        # print("=" * 50)

        soup = BeautifulSoup(
            response.content,
            "html.parser"
        )

        # ----------------------------------------------------
        # article 태그
        # ----------------------------------------------------
        # find("article") : BeautifulSoup 객체의 메소드
        # 매개변수인 문자열에 해당하는 태그를 찾는 메소드
        article = soup.find("article")

        if article:
            # html의 태그들을 버리고 순수하게 글자만 가져오는 것
            return article.get_text(
                separator=" ",
                strip=True,
            )

        # ----------------------------------------------------
        # div(CmAdContent)
        # ----------------------------------------------------
        # <div id="CmAdContent"> 를 찾아라
        article = soup.find(
            "div",
            id="CmAdContent",
        )

        if article:

            return article.get_text(
                separator=" ",
                strip=True,
            )

        # ----------------------------------------------------
        # body
        # ----------------------------------------------------

        body = soup.find("body")

        if body:

            return body.get_text(
                separator=" ",
                strip=True,
            )

        return "기사 내용을 찾을 수 없습니다."

    except Exception as err:
        return f"오류 : {err}"
# ============================================================
# 기사 목록들을 하나의 문자열로 합칩니다.
# ============================================================
def merge_articles(article_list):
    # 의미가 있는 기사 내용만 목록에 포함 시키기 위하여 if 구문 사용함
    clean_articles = [article for article in article_list if article]

    return DOCUMENT_SEPARATOR.join(clean_articles)


# DOCUMENT_SEPARATOR
