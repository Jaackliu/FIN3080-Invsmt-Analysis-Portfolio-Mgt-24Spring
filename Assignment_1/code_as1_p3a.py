
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/problem3_data.csv')
df.columns = ['stock_code', 'date', 'revenue', 'ROE']
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df = df[(df['year'] >= 2010) & (df['year'] <= 2020)]

# calculate annual median values for ROE
df.dropna(subset=['ROE', 'revenue'], inplace=True)
complete_firms = df.groupby('stock_code').filter(lambda x: set(x['year']) == set(range(2010, 2021)))
complete_firms.sort_values(by=['stock_code', 'year'], inplace=True)
roe_median = complete_firms.groupby('year')['ROE'].median()
complete_firms['revenue_growth'] = complete_firms.groupby('stock_code')['revenue'].pct_change().fillna(0) * 100

years = list(range(2010, 2021))
firmList = set(complete_firms['stock_code'].unique())
cons_above_roe = firmList.copy()
cons_above_rev_growth = firmList.copy()
pct_above_median_roe = [50]  # Initialize with 50% for the first year
pct_above_growth_rate = [50]

# print(roe_median.dtypes)


for year in years[1:]:
    median_roe_for_year = roe_median.loc[year]
    median_growth_rate_for_year = complete_firms[complete_firms['year'] == year]['revenue_growth'].median()

    current_above_roe = set(complete_firms[(complete_firms['year'] == year) & (complete_firms['ROE'] > median_roe_for_year)]['stock_code'])
    current_above_rev_growth = set(complete_firms[(complete_firms['year'] == year) & (complete_firms['revenue_growth'] > median_growth_rate_for_year)]['stock_code'])

    cons_above_roe &= current_above_roe
    cons_above_rev_growth &= current_above_rev_growth

    pct_above_median_roe.append(len(cons_above_roe) / len(firmList) * 100)
    pct_above_growth_rate.append(len(cons_above_rev_growth) / len(firmList) * 100)


plt.figure(figsize=(12, 6))
plt.plot(years, pct_above_median_roe, label='Percentage of Firms Consistently Above Median ROE')
plt.plot(years, pct_above_growth_rate, label='Percentage of Firms Consistently Above Median Revenue Growth')
plt.title('Percentage of Firms Consistently Outperforming Market Median')
plt.xlabel('year')
plt.ylabel('percentage')
plt.ylim(0, 60)  # Adjusted for full percentage scale
plt.xticks(years[0:])
plt.legend()
plt.grid(True)
plt.show()
