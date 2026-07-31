# Youtube 요약
# pip install youtube-search
# pip install youtube_transcript_api
import os
import matplotlib.pyplot as plt

from youtube_search import YoutubeSearch
from langchain_community.document_loaders import YoutubeLoader
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from konlpy.tag import Okt
from collections import Counter

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

keyword = '6.3 선거'
videos = YoutubeSearch(keyword, max_results=5).to_dict()

# duration이 int인 경우 문자열로 변경
for v in videos:

    if isinstance(v['duration'], int):
        v['duration'] = str(v['duration'])

# videos
# YouTube 검색 결과를 보기 좋게 출력하는 함수
def print_youtube_results(videos):
    # 검색 결과가 없는 경우 처리
    if not videos:
        print("검색 결과가 없습니다.")
        return

    # 각 영상 정보를 반복 출력
    for idx, video in enumerate(videos, start=1):

        # 안전하게 값 가져오기
        title = video.get("title", "제목 없음")
        channel = video.get("channel", "채널 정보 없음")
        views = video.get("views", "조회수 정보 없음")
        publish_time = video.get("publish_time", "업로드 정보 없음")
        duration = video.get("duration", "재생시간 정보 없음")
        content = video.get("content", "내용 없음")

        # YouTube 링크 생성
        url_suffix = video.get("url_suffix", "")
        youtube_url = "https://www.youtube.com" + url_suffix

        # 출력
        print("=" * 80)
        print(f"[{idx}] 제목 : {title}")
        print(f"채널명 : {channel}")
        print(f"재생시간 : {duration}")
        print(f"조회수 : {views}")
        print(f"업로드 : {publish_time}")
        print(f"링크 : {youtube_url}")
        print(f"컨텐츠 : \n{content}")

    print("=" * 80)

# 함수 호출
print_youtube_results(videos)


# 임의의 요소 1개의 url 정보
video_url = 'http://youtube.com' + videos[3]['url_suffix']
video_url

loader = YoutubeLoader.from_youtube_url(
    video_url, 
    language=['ko', 'en'] # 자막 언어
)

loader.load()

for v in videos:
    # url_suffix를 이용하여 video_url을 만듭니다.
    v['video_url'] = 'https://youtube.com' + v['url_suffix']

    # YoutubeLoader를 이용하여 비디오를 로드합니다.
    loader = YoutubeLoader.from_youtube_url(
        v['video_url'],
        language=['ko', 'en']
    )

    v['content'] = loader.load()

print_youtube_results(videos)

print('총 영상 수:', len(videos))
# 영상 길이가 60분 이하인 영상만 남깁니다. 
videos = [v for v in videos if len(v['duration'].split(':')) < 3]
print('60분 이하 영상 개수 :', len(videos))

# 랭체인, openai 임포트
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
model.invoke('안녕?') # 언어 모델이 잘 설정되었는지 테스트

# 동영상 요약 프롬프트 작성
# 감성 분석 추가 : 선거/정치 분석에 매우 좋음
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            다음 유튜브 영상 내용을 분석하여:

            - 핵심 주제
            - 긍정/부정 분위기
            - 주요 키워드
            - 자주 언급된 인물
            - 핵심 쟁점

            을 정리해줘.

            {context}
            """
        )
    ]
)

chain = create_stuff_documents_chain(model, prompt)

result = chain.invoke({"context": videos[0]['content']})
result

# 모든 비디오에 대해 요약을 생성
from tqdm import tqdm # tqdm은 진행 상황을 보여주는 라이브러리

for v in tqdm(videos):
    v['summary'] = chain.invoke({"context": v['content']})

print_youtube_results(videos)

# 모든 content 합치기
all_text = ""

for v in videos:
    content = v.get('content')

    if content:
        # Document 객체 처리
        if isinstance(content, list):
            for doc in content:
                all_text += doc.page_content + " "

# 불용어를 읽어서, 명사 추출하기
with open("stopword.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)


okt = Okt()
nouns = okt.nouns(all_text)

# 불용어 제거 + 2글자 이상
filtered_words = [
    word for word in nouns

    if len(word) > 1
    and word not in stopwords
]

# 빈도수 계산
counter = Counter(filtered_words)

topN = counter.most_common(10)

print(topN)


# 그래프 그리기
words = [x[0] for x in topN]
counts = [x[1] for x in topN]

plt.figure(figsize=(10, 5))

plt.bar(words, counts)

plt.title("유튜브 키워드 빈도수 TOP10")

plt.xlabel("키워드")
plt.ylabel("빈도수")

plt.xticks(rotation=45)

plt.show()