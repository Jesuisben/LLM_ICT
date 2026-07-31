# =====================================================================
# 키워드 추출 및 시각화와 관련된 모듈
# =====================================================================
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rcParams["axes.unicode_minus"] = False

from konlpy.tag import Okt
from collections import Counter
# =====================================================================
# 영상에서 키워드를 top_n개 추출하여 [(단어, 빈도수), ...]을 반환합니다.
# 불용어에 사용할 파일은 stopword_path를 참조합니다.
# =====================================================================
def extract_keywords(
    videos, stopword_path='stopword.txt', top_n=10
):
    all_text = ''

    for video in videos : # 모든 자막 합치기
        caption_info = video.get('content')

        if not caption_info:
            continue # 이 영상에는 캡션 정보 없음

        for doc in caption_info:
            all_text += doc.page_content + " "

    if not all_text.strip():
        return [] # 공백 문자만 있으면 빈 list 반환

    stopwords = load_stopwords(stopword_path)

    okt = Okt()

    nouns = okt.nouns(phrase=all_text)

    # 글자 길이가 2자리 이상이고, 불용어(stopwords) 목록에 포함되지 않는 단어들
    word_list = [word for word in nouns
        if len(word) >= 2
        and word not in stopwords
    ]

    counter = Counter(word_list)

    return counter.most_common(top_n)
# =====================================================================
# 불용어 목록 파일에서 불용어를 읽어 들입니다.
# =====================================================================
def load_stopwords(stopword_path):
    with open(stopword_path, mode='rt', encoding='UTF-8') as stop_file:
        return set(line.strip() for line in stop_file)
# =====================================================================
# 키워드 빈도수를 사용하여 그래프 객체(Figure)를 생성합니다.
# =====================================================================
def draw_keyword_chart(top_keywords):
    fig, ax = plt.subplots(figsize=(10, 5))

    if not top_keywords:
        ax.text(
            0.5,
            0.5,
            "No Keyword",
            ha="center",
            va="center",
            fontsize=15
        )

        ax.set_axis_off()

        return fig


    words = [x[0] for x in top_keywords]
    counts = [x[1] for x in top_keywords]

    ax.bar(words, counts)

    ax.set_title("YouTube Keyword Frequency TOP10")

    ax.set_xlabel("Keyword")

    ax.set_ylabel("Frequency")

    plt.setp(ax.get_xticklabels(), rotation=45)

    fig.tight_layout()

    return fig
# ===== End Of File ======================================================