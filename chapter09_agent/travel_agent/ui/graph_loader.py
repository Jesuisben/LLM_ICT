import streamlit as st

from langchain_openai import ChatOpenAI

from chapter09_agent.travel_agent.graph.workflow import create_graph

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

# ------------------------------------------------
# LangGraph 생성
#
# 최초 한 번만 생성되고,
# 이후에는 캐시된 객체를 사용한다.
# ------------------------------------------------

@st.cache_resource
def load_graph():

    model = ChatOpenAI(
        model="gpt-4o", api_key=api_key
    )

    return create_graph(model)