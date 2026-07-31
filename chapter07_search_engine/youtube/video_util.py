# =====================================================================
# Video와 관련된 모듈
# =====================================================================
import streamlit as st
# =====================================================================
# 검색된 영상 목록을 출력합니다.
# =====================================================================
def show_videos(video_dict):
    if not video_dict:
        st.warning('검색된 결과가 없습니다.')
        return

    st.markdown(f'## 검색 결과 ({len(video_dict)}개)')

    for idx, video in enumerate(video_dict, start=1):
        with st.expander(f'{idx}. {video["title"]}', expanded=False):
            view_video(video)
# =====================================================================
# 해당 영상에 대한 정보를 출력합니다.
# =====================================================================
def view_video(video):
    with st.container(border=True):
        st.subheader(video.get('title', "No Title"))

        col1, col2 = st.columns([1, 2])

        with col1:
            # 해당 유투브의 대표 이미지를 보여주는 코드(using Youtube ID)
            thumbnail = f'https://img.youtube.com/vi/{video.get("id", "")}/0.jpg'
            st.image(thumbnail, width="content")

        with col2:
            st.write(f'**채널명** : {video.get("channel", "")}')
            st.write(f'**재생 시간** : {video.get("duration", "")}')
            st.write(f'**조회수** : {video.get("views", "")}')
            st.write(f'**업로드** : {video.get("publish_time", "")}')
            # print("video['video_url']")
            # print(video['video_url'])
            st.link_button(' ▶ YouTube 보기', video['video_url'])
# =====================================================================
# 해당 영상과 요약을 동시에 출력합니다.
# =====================================================================
def show_video_summary(video):
    st.divider()

    st.markdown("## 📄 영상 요약")

    summary = video.get('summary', '')

    if not summary:
        st.info('요약된 결과가 없습니다.')
        return
    else:
        st.markdown(summary)
# =====================================================================
# 키워드 분석 결과를 그래프로 그리고, markdown으로 순위를 출력합니다.
# =====================================================================
def show_keyword_result(top_keywords, fig):
    st.markdown("## 🔑 키워드 분석")

    if not top_keywords:
        st.info('분석할 키워드가 없습니다.')
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.pyplot(fig)

    with col2:
        st.markdown('### Top Keyword')

        rank = 1 # for 랭킹

        for word, count in top_keywords:
            st.write(f'{rank}. **{word}** ({count})')
            rank += 1

# ===== End Of File ======================================================