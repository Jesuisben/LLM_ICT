# =====================================================================
# YouTube 검색 및 자막 로딩을 위한 모듈입니다.
# =====================================================================
import os, re

from langchain_community.document_loaders import YoutubeLoader
from youtube_search import YoutubeSearch
# =====================================================================
# 검색 키워드와 읽을 영상 개수를 입력하여 YouTube 목록을 dict로 반환합니다.
# =====================================================================
def search_youtube(
    keyword:str,
    max_results: int = 5
) -> dict:
    video_dict = YoutubeSearch(keyword, max_results).to_dict()

    # print('video_dict')
    # print(video_dict)
    # print('='*80)

    URL_PREFIX = 'https://www.youtube.com' # 유투브 주소 접두사

    # 데이터 전처리
    for video in video_dict:
        # 영상 길이의 데이터 타입 통일(모두 str 타입으로..__예시 : 5:48)
        if isinstance(video.get('duration'), int):
            video['duration'] = str(video['duration'])

        # 해당 주소의 full url 생성
        video['video_url'] = URL_PREFIX + video.get('url_suffix')

        # 이후에 사용할 변수들 초기화
        video['content'] = None # 자막 정보
        video['summary'] = '' # 요약 정보

    return video_dict
# =====================================================================
# 모든 영상들의 자막을 읽습니다.
# =====================================================================
def load_all_caption(video_dict, language=None):
    if language is None:
        language = ['ko', 'en']

    # 저장할 폴더 생성
    save_dir = "captions"
    os.makedirs(save_dir, exist_ok=True)

    for video in video_dict:
        documents = load_caption(video['video_url'], language)
        video['content'] = documents
        # print("for debugging video['content']")
        # print(video['content'])
        # print('='*80)

        # ---------------------------------------
        # 파일명으로 사용할 수 없는 문자 제거
        # ---------------------------------------
        filename = re.sub(r'[\\/:*?"<>|]','_', video['title'])

        filepath = os.path.join(
            save_dir,
            f"{filename}.txt"
        )

        # ---------------------------------------
        # 자막 저장
        # ---------------------------------------
        with open(filepath, "wt", encoding="utf-8") as myfile:
            myfile.write(str(video['content']))

    return video_dict
# =====================================================================
# 해당 영상의 자막을 읽어 와서, LangChain의 Document 객체 형식으로 반환합니다.
# =====================================================================
def load_caption(url, lang=None):
    if lang is None:
        lang = ['ko', 'en']

    try:
        loader = YoutubeLoader.from_youtube_url(
            youtube_url=url,
            language=lang
        )
        docs = loader.load()

        return docs
    except Exception as err :
        print(f'Caption Load Error : {err}')
        return []

# ===== End Of File ======================================================