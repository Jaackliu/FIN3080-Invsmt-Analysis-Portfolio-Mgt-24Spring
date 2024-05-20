
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/problem3_data.csv')
df.columns = ['stock_code', 'date', 'revenue', 'ROE']
df['date'] = pd.to_datetime(df['date'])

# calculate annual median values for ROE
df['year'] = df['date'].dt.year
df = df[(df['Year'] >= 2011) & (df['Year'] <= 2020)]
df_median = df.groupby('year')['ROE'].median().reset_index()
df_median.columns = ['year', 'ROE_median']


# calculate annual median values for total revenue growth rate, merge with df_median
df['revenue_growth'] = df['revenue'].pct_change()
df_revenue_growth = df.groupby('year')['revenue_growth'].median().reset_index()
df_revenue_growth.columns = ['year', 'revenue_growth_median']
df_median = df_median.merge(df_revenue_growth, on='year')

# # round median values to 4 decimal places
# df_median = df_median.round(4)
# df_median.to_csv('AS_1_p3_median.csv')

# calculate percentages of companies that consistently maintain above-median ROE over 2011 to 2020
df_merged = pd.merge(df, df_median, on='year')
df_merged['roe_above_median'] = df_merged['ROE'] > df_merged['ROE_median']
df_merged['growth_above_median'] = df_merged['revenue_growth'] > df_merged['revenue_growth_median']
roe_result_list = []
growth_result_list = []