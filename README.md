# 基于混合整数线性规划的学校课表优化安排模型

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

本项目旨在使用混合整数线性规划(MILP)方法优化中学课程表安排，以最小化学生疲劳度为目标，同时满足多种教学约束。

## 项目背景

传统人工排课方式难以平衡学生学科能力差异、教师时间冲突等多重约束。本研究以广东省揭阳第一中学为实践场景，构建基于MILP的课表优化模型，通过分析学生历史成绩与学科能力差异，实现课表编排的全局优化。

## 主要功能

- 基于学生成绩数据计算学科权重
- 考虑课程连贯性和学生疲劳度
- 满足多种排课约束
- 使用OR-Tools CP-SAT求解器进行优化

## 安装与使用

### 依赖安装

```bash
pip install ortools==9.12.4544
pip install pandas==2.0.3
pip install numpy==1.24.4
pip install scipy==1.10.1
```
或者
```bash
pip install -r requirements.txt
```

### 使用步骤

1. 准备学生成绩数据（示例见`scores.xlsx`）
2. 运行权重计算：
   ```bash
   python count.py
   ```
3. 按需更改`arrange.py`中的数据
4. 运行课表优化：
   ```bash
   python arrange.py
   ```
5. 查看结果（生成`课表安排.txt`）

## 文件说明

- `count.py`: 计算各科目权重和周课时数
- `arrange.py`: 主优化程序，生成最优课表
- `scores.xlsx`: 示例学生成绩数据（需按实际修改）

## 模型特点

- **目标函数**: 最小化学生总疲劳度
- **约束条件**:
  - 总课时约束
  - 时间冲突约束
  - 体育课优先下午最后一节
  - 核心科目每日最低课时
  - 连堂限制等

## 结果示例

优化后课表示例：
```
一班：
星期一
第一节: 班会
第二节: 数学
第三节: 语文
...
```

疲劳度对比：
| 班级 | 优化前 | 优化后 | 降低比例 |
|------|--------|--------|----------|
| 1班  | 278.5  | 271.1  | 2.657%   |
| 2班  | 277.5  | 266.75 | 3.837%   |

## 贡献指南

欢迎提交[Issue](https://github.com/Jessssssseea/Optimization-Model-of-School-Schedule-Arrangement-Based-on-Mixed-Integer-Linear-Programming/issues)或[Pull Request](https://github.com/Jessssssseea/Optimization-Model-of-School-Schedule-Arrangement-Based-on-Mixed-Integer-Linear-Programming/pulls)。

## 许可证

本项目采用MIT许可证 - 详见[LICENSE.md](https://github.com/Jessssssseea/Optimization-Model-of-School-Schedule-Arrangement-Based-on-Mixed-Integer-Linear-Programming/blob/main/LICENSE.md)文件

## 致谢

感谢指导教师杨一慧老师和黄纯洁老师的指导！
