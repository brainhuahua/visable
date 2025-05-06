##处理数据
import pandas as pd
import numpy as np
import os

# 设置路径（请根据你本地文件路径修改）
basePath = f'data'

cleanPath = f'data_clean'

def clean_data(base_path=basePath,clean_path=cleanPath):
    # 1. 读取学生信息表并处理缺失值
    student_df = pd.read_csv(os.path.join(base_path, 'Data_StudentInfo.csv'))
    student_df.dropna(subset=['student_ID'], inplace=True)  # 删除 student_ID 缺失行
    student_df['sex'] = student_df['sex'].fillna('')
    student_df['age'] = student_df['age'].fillna(student_df['age'].median())
    student_df['major'] = student_df['major'].fillna('')

    student_df.to_csv(os.path.join(clean_path, 'Data_StudentInfo.csv'), index=False)

    # 2. 读取题目信息表并处理缺失值
    title_df = pd.read_csv(os.path.join(base_path, 'Data_TitleInfo.csv'))
    title_df.dropna(subset=['title_ID'], inplace=True)
    title_df['knowledge'] = title_df['knowledge'].fillna('')
    title_df['sub_knowledge'] = title_df['sub_knowledge'].fillna('')

    title_df.to_csv(os.path.join(clean_path, 'Data_TitleInfo.csv'), index=False)

    # 3. 合并所有班级的答题记录日志
    log_path = os.path.join(base_path, 'Data_SubmitRecord')
    log_files = os.listdir(log_path)

    log_list = []
    for file in log_files:
        file_path = os.path.join(log_path, file)
        df = pd.read_csv(file_path)
        df['class'] = file.split('.')[0]  # 添加班级列,同时对班级数列异常值进行处理
        log_list.append(df)

    submit_df = pd.concat(log_list, ignore_index=True)

    submit_df.to_csv(os.path.join(base_path, 'Data_SubmitRecord.csv'), index=False)

    # 4. 答题记录日志的缺失值处理
    submit_df.dropna(subset=['student_ID', 'title_ID', 'time'], inplace=True)

    # 5. 数值型字段处理与异常值剔除
    submit_df['score'] = pd.to_numeric(submit_df['score'], errors='coerce').fillna(0)
    submit_df['memory'] = pd.to_numeric(submit_df['memory'], errors='coerce')
    submit_df['timeconsume'] = pd.to_numeric(submit_df['timeconsume'], errors='coerce')

    submit_df = submit_df[submit_df['score'] >= 0]
    submit_df = submit_df[submit_df['memory'].fillna(0) >= 0]
    submit_df = submit_df[submit_df['timeconsume'].fillna(0) >= 0]

    # 6. 类别字段处理
    submit_df['method'] = submit_df['method'].str.lower().str.strip().fillna('unknown')
    submit_df['state'] = submit_df['state'].fillna('unknown')

    submit_df.to_csv(os.path.join(clean_path, 'Data_SubmitRecord.csv'), index=False)

clean_data(base_path=basePath, clean_path=cleanPath)