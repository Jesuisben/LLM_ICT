# ============================================================
# Video와 관련된 모듈
# ============================================================
import streamlit as st
# ============================================================
# 검색된 영상 목록을 출력합니다.
# ============================================================
def show_videos(video_dict):
    if not video_dict:
        st.warning("검색된 결과가 없습니다.")
        return

    st.markdown(f"## 검색 결과 ({len(video_dict)}개")

    for idx, video in enumerate(video_dict, start=1):
        with st.expander(f"{idx}. {video['title']}", expanded=False):
            view_video(video)

# ============================================================
# 해당 영상에 대한 정보를 출력합니다.
# ============================================================
def view_video(video):
    with st.container(border=True):
        st.subheader(video.get("title", "No Title"))

        # 비율을 1대 2로 나누는 것 (html에서 비율로 영역 설정하는 느낌)
        col1, col2 = st.columns([1, 2])

        with col1:
            # 해당 유투브의 대표 이미지를 보여주는 코드(using Youtube ID)
            thumbnail = f'https://img.youtube.com/vi/{video.get("id", "")}/0.jpg'
            st.image(thumbnail, use_container_width=True)

        with col2:
            st.write(f'**채널명** : {video.get("channel", "")}')
            st.write(f' ** 재생 시간 ** : {video.get("duration", "")}')
            st.write(f' ** 조회수 ** : {video.get("views", "")}')
            st.write(f' ** 업로드 ** : {video.get("publish_time", "")}')

            st.link_button("▶ YouTube 보기", video["video_url"])