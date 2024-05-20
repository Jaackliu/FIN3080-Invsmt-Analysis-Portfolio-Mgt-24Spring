import pandas as pd

# 生成从 2000Q1 到 2023Q3 的 Period 数据
periods = pd.period_range(start='2000Q1', end='2023Q3', freq='Q')

# 将 Period 数据转换为 DataFrame
quarter_list = pd.DataFrame({'date': periods})

# 将 DataFrame 保存为 CSV 文件
quarter_list.to_csv('quarter_list.csv', index=False)