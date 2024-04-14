import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# 欢迎来到数据分析平台! 👋")

st.sidebar.success("选择一项功能.")

st.markdown(
    """
    是一个简单的用来进行分数分析的平台,现在设置为可以分析grade6的成绩
    
    **👈 Select  from the sidebar** 
    
"""
)