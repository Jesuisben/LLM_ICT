import streamlit as st
import pandas as pd

st.header("가전 제품 판매량 예제")

# 가전 제품 데이터 생성
data = pd.DataFrame({
    '가전제품': ['냉장고', '세탁기', 'TV', '전자레인지', '에어컨'],
    '판매량': [120, 95, 150, 80, 110]
})

# 데이터 표 출력
st.dataframe(data)

# 막대 그래프 출력
st.bar_chart(data.set_index('가전제품'))