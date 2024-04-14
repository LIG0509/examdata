import streamlit as st

def main():
    st.title('文件上传')
    uploaded_file = st.file_uploader("选择一个Excel文件", type=['xlsx'])
    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file  # 存储上传的文件
        st.success("文件上传成功！")

if __name__ == "__main__":
    main()
