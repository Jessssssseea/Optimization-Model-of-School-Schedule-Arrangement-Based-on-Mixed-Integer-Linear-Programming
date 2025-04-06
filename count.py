import pandas as pd
import numpy as np
from scipy.stats import skew

def calculate_weights(df_subject, main_subjects):
    """计算科目综合权重"""
    # 基础指标
    metrics = {
        'mean': df_subject.mean(),
        'std': df_subject.std(),
        'skew': df_subject.skew(),
        'floor_rate': (df_subject < 60).mean()  # 低分率
    }
    
    # 指标标准化（0-1范围）
    scaled = {}
    for k, v in metrics.items():
        if k in ['mean', 'skew']:  # 需反向处理的指标
            scaled[k] = (v.max() - v) / (v.max() - v.min()) if v.max() != v.min() else 0.5
        else:
            scaled[k] = (v - v.min()) / (v.max() - v.min()) if v.max() != v.min() else 0.5
    
    # 综合权重公式（可调整系数）
    return (
        0.4 * (1 - scaled['mean']) +      # 平均分权重40%
        0.25 * scaled['std'] +           # 标准差权重25%
        0.2 * (1 + scaled['skew']) +      # 偏态系数权重20% 
        0.15 * scaled['floor_rate']      # 低分率权重15%
    )

def analyze_schedule():
    # 读取数据并预处理
    df = pd.read_excel('scores.xlsx')
    main_subjects = ['chinese', 'math', 'english']
    science_subjects = ['physics', 'chemistry', 'biology']
    arts_subjects = ['history', 'politics', 'geography']
    
    for class_name, group in df.groupby('class'):
        # 数据标准化处理（主科转换为百分制）
        converted = group.copy()
        converted[main_subjects] = converted[main_subjects] / 1.5
        
        # 计算学科关联矩阵
        corr_matrix = converted[main_subjects + science_subjects + arts_subjects].corr()
        
        # 初始化基础课时
        schedule = {
            '语文': 5, '数学': 6, '外语': 5,    # 主科基础
            '物理': 3, '化学': 3, '生物学': 2,    # 理科基础
            '历史': 2, '思想政治': 1, '地理': 1,    # 文科基础
            '体育与健康': 2, '音乐或心理': 1, '信息技术': 1, '通用技术': 1 # 固定科目                     # 固定课时
        }
        
        # 计算剩余可分配课时
        remaining = 39 - sum(schedule.values())
        
        # 生成权重数据集
        weight_dict = {}
        subjects = main_subjects + science_subjects
        
        for subj in subjects:
            # 本科目成绩分析
            subject_weights = calculate_weights(converted[subj], main_subjects)
            
            # 关联学科影响（取相关度最高的3科）
            correlations = corr_matrix[subj].drop(subj).nlargest(3)
            related_impact = correlations.mean() * 0.3  # 相关影响系数
            
            # 最终权重计算
            weight_dict[subj] = subject_weights * (1 + related_impact)
        
        # 标准化权重分配
        total_weight = sum(weight_dict.values())
        allocation = {k: round(v/total_weight*remaining) for k,v in weight_dict.items()}
        
        # 分配课时并调整
        for subj in subjects:
            schedule[subj_map[subj]] += allocation.get(subj, 0)
        
        # 最终平衡处理
        adjust_schedule(schedule)
        
        # 输出结果
        print(f"\n班级 {class_name} 周课时安排：")
        for subject, hours in sorted(schedule.items(), key=lambda x: -x[1]):
            print(f"{subject}: {hours}节")

def adjust_schedule(schedule):
    """平衡调整确保总课时正确"""
    total = sum(schedule.values())
    if total != 39:
        # 找到可调整的主科
        main_subjs = ['语文', '数学', '外语']
        diff = 39 - total
        adjust_subj = max(main_subjs, key=lambda x: schedule[x])
        schedule[adjust_subj] += diff

# 科目名称映射
subj_map = {
    'chinese': '语文',
    'math': '数学',
    'english': '外语',
    'physics': '物理',
    'chemistry': '化学',
    'biology': '生物学',
    'history': '历史',
    'politics': '思想政治',
    'geography': '地理'
}

if __name__ == "__main__":
    analyze_schedule()
