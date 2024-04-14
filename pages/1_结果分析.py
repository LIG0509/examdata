import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['WenQuanYi Zen Hei']
def main():
    st.title('结果分析')

    if 'uploaded_file' in st.session_state and st.session_state['uploaded_file'] is not None:
        df = pd.read_excel(st.session_state['uploaded_file'])

        # 提取答案列
        single_choice_score_columns = [col for col in df.columns if col.startswith('一')]
        two_stage_choice_score_columns = [col for col in df.columns if col.startswith('二')]
        all_score_columns = single_choice_score_columns + two_stage_choice_score_columns

        # 计算总分
        df['选择题总分'] = df[all_score_columns].sum(axis=1)
        df['单选题总分'] = df[single_choice_score_columns].sum(axis=1)
        df['二阶选择题总分'] = df[two_stage_choice_score_columns].sum(axis=1)

        # 计算选择题的统计指标并转置
        stats_data = {
            '选择题总分': df['选择题总分'].agg(['mean', 'std', 'max', 'min', 'median']).round(3),
            '单选题总分': df['单选题总分'].agg(['mean', 'std', 'max', 'min', 'median']).round(3),
            '二阶选择题总分': df['二阶选择题总分'].agg(['mean', 'std', 'max', 'min', 'median']).round(3)
        }
        stats_df = pd.DataFrame(stats_data).transpose()  # 转置 DataFrame
        stats_df.columns = ['均值', '标准差', '最大值', '最小值', '中位数']  # 重命名列
        st.dataframe(stats_df)  # 使用 dataframe 以得到更好的布局和格式

        # 将二阶选择题分组并计算统计数据
        group_stats = {}
        for col in two_stage_choice_score_columns:
            group_number = col[1]  # 假设第二字符是组号
            if group_number not in group_stats:
                group_stats[group_number] = []
            group_stats[group_number].append(col)

        # 计算每组题目的统计数据并转置
        for group, columns in group_stats.items():
            group_total = df[columns].sum(axis=1)
            group_stats = group_total.agg(['mean', 'std', 'max', 'min', 'median']).round(3)
            st.write(f"组{group}二阶选择题统计数据:")
            st.dataframe(pd.DataFrame(group_stats).transpose())  # 显示每组的数据


        # 设置统一的直方图样式
        plt.style.use('grayscale')

        # 绘制选择题总分的分布直方图
        plt.figure(figsize=(10, 6))
        plt.hist(df['选择题总分'], bins=range(min(df['选择题总分']), max(df['选择题总分']) + 1, 1),
                 color='black', edgecolor='white')
        plt.title('选择题总分分布')
        plt.xlabel('总分')
        plt.ylabel('学生数量')
        plt.ylim(0, 800)
        st.pyplot(plt)

        # 绘制单选题总分的分布直方图
        plt.figure(figsize=(10, 6))
        plt.hist(df['单选题总分'], bins=range(min(df['单选题总分']), max(df['单选题总分']) + 1, 1),
                 color='black', edgecolor='white')
        plt.title('单选题总分分布')
        plt.xlabel('总分')
        plt.ylabel('学生数量')
        plt.ylim(0, 800)
        st.pyplot(plt)

        # 绘制二阶选择题总分的分布直方图
        plt.figure(figsize=(10, 6))
        plt.hist(df['二阶选择题总分'], bins=range(min(df['二阶选择题总分']), max(df['二阶选择题总分']) + 1, 1),
                 color='black', edgecolor='white')
        plt.title('二阶选择题总分分布')
        plt.xlabel('总分')
        plt.ylabel('学生数量')
        plt.ylim(0, 800)
        st.pyplot(plt)


    else:
        st.warning("请先上传文件。")

if __name__ == "__main__":
    main()
