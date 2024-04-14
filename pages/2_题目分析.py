import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 指定默认字体
plt.rcParams['font.family'] = ['WenQuanYi Zen Hei']

def calculate_statistics(df):
    all_score_columns = [col for col in df.columns if col.startswith('一') or col.startswith('二')]
    data = {
        '题目': [],
        '平均分': [round(df[col].mean(), 3) for col in all_score_columns],
        '标准差': [round(df[col].std(), 3) for col in all_score_columns],
        '区分度': [],
        '删除项后信度': []
    }

    df['总分'] = df[all_score_columns].sum(axis=1)
    upper_quartile = df['总分'].quantile(0.73)
    lower_quartile = df['总分'].quantile(0.27)
    high_group = df[df['总分'] >= upper_quartile]
    low_group = df[df['总分'] <= lower_quartile]

    for column in all_score_columns:
        data['题目'].append(column)
        high_avg = high_group[column].mean()
        low_avg = low_group[column].mean()
        data['区分度'].append(round(high_avg - low_avg, 3))
        temp_items = [col for col in all_score_columns if col != column]
        data['删除项后信度'].append(round(cronbach_alpha(df[temp_items]), 3))

    return pd.DataFrame(data)

def cronbach_alpha(items_scores):
    items_count = items_scores.shape[1]
    total_var = items_scores.var(ddof=1, axis=0).sum()
    total_scores_var = items_scores.sum(axis=1).var(ddof=1)
    return round((items_count / (items_count - 1)) * (1 - (total_var / total_scores_var)), 3)

def plot_answer_distribution(df):
    single_choice_answer_columns = [col for col in df.columns if col.startswith('答案(一')]
    two_stage_choice_answer_columns = [col for col in df.columns if col.startswith('答案(二')]
    all_answer_columns = single_choice_answer_columns + two_stage_choice_answer_columns
    correct_answers = ['D', 'C', 'C', 'C', 'A', 'D', 'B', 'B', 'B', 'A', 'D', 'B', 'C', 'C', 'D', 'C', 'D', 'B', 'A', 'A']
    plt.figure(figsize=(10, len(all_answer_columns) * 0.5))
    colors = ['#add8e6', '#ffcccb', '#90ee90', 'yellow']
    for index, (column, correct_answer) in enumerate(zip(reversed(all_answer_columns), reversed(correct_answers))):
        answers = df[column].value_counts(normalize=True).reindex(['A', 'B', 'C', 'D'], fill_value=0) * 100
        bottom = 0
        for answer, color in zip(['A', 'B', 'C', 'D'], colors):
            bar_width = answers[answer]
            plt.barh(index, bar_width, left=bottom, color=color)
            if answer == correct_answer:
                plt.text(bottom + bar_width / 2, index, f'{bar_width:.1f}%', ha='center', va='center', color='black')
            bottom += bar_width
    plt.yticks(np.arange(len(all_answer_columns)), reversed(all_answer_columns))
    plt.legend(['A', 'B', 'C', 'D'], title='答案选项', loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=4)
    plt.xlabel('百分比 (%)')
    plt.title('每个题目的答案选项分布')
    plt.tight_layout()
    st.pyplot(plt)

def main():
    st.title('题目统计分析')

    if 'uploaded_file' in st.session_state:
        df = pd.read_excel(st.session_state['uploaded_file'])
        statistics_df = calculate_statistics(df)
        st.table(statistics_df)
        plot_answer_distribution(df)
    else:
        st.warning("请先页面上传文件。")

if __name__ == "__main__":
    main()
