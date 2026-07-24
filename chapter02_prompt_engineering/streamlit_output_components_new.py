import streamlit as st
import pandas as pd

st.header("가전 제품 판매량 예제")

data = pd.DataFrame({
    '가전제품': ['냉장고', '세탁기', 'TV', '전자레인지', '에어컨'],
    '판매량': [120, 95, 150, 80, 110]
})

st.dataframe(data) # 표 출력

chart_data = data.set_index("가전제품")

st.subheader("막대 그래프")
st.bar_chart(chart_data)

st.divider()

st.subheader("꺾은선 그래프")
st.line_chart(chart_data)