
import pandas as pd
import matplotlib.pyplot as plt


""" read files and basic data cleaning """


price_value_return = pd.read_csv('data/Monthly Return/TRD_Mnth.csv')
# EPS_bookValue = pd.read_csv('data/Index per Share/FI_T9.csv')
EPS_bookValue = pd.read_csv('data/Index per Share-TTM/FI_T9.csv')
RnD = pd.read_csv('data/Income Statement/FS_Comins.csv')
ROA_ROE = pd.read_csv('data/Earning Capacity/FI_T5.csv')
estDate_type = pd.read_csv('data/Company Profile/TRD_Co.csv')
asset_liability = pd.read_csv('data/Balance Sheet/FS_Combas.csv')
quarter_list = pd.read_csv('data/quarter_list.csv')


# delete all the rows including "B" in the Typrep column
asset_liability = asset_liability[asset_liability['Typrep'] != 'B']
EPS_bookValue = EPS_bookValue[EPS_bookValue['Typrep'] != 'B']
RnD = RnD[RnD['Typrep'] != 'B']
ROA_ROE = ROA_ROE[ROA_ROE['Typrep'] != 'B']


# drop Typrep column
asset_liability = asset_liability.drop(columns=['Typrep'])
EPS_bookValue = EPS_bookValue.drop(columns=['Typrep'])
RnD = RnD.drop(columns=['Typrep'])
ROA_ROE = ROA_ROE.drop(columns=['Typrep'])


""" derive monthly P/E ratios, monthly P/B ratios """

# rename columns
price_value_return.columns = ['stock_code', 'date', 'closing_price',
                              'market_value', 'return']
EPS_bookValue = EPS_bookValue.drop(columns=['ShortName_EN'])
EPS_bookValue.columns = ['stock_code', 'date', 'earnings_per_share', 'book_value_per_share']


# convert "date" column to period type
price_value_return['date'] = pd.to_datetime(price_value_return['date']).dt.to_period('M')
EPS_bookValue['date'] = pd.to_datetime(EPS_bookValue['date']).dt.to_period('M')
EPS_bookValue['date'] = (EPS_bookValue['date'].dt.to_timestamp() + pd.DateOffset(months=1)).dt.to_period('M')


# merge price_value_return and EPS_bookValue
merged_df_1 = pd.merge(price_value_return, EPS_bookValue, on=['stock_code', 'date'], how='left')


# fill missing values in "earnings_per_share" and "book_value_per_share" columns
merged_df_1['earnings_per_share'] = merged_df_1.groupby('stock_code')['earnings_per_share'].ffill()
merged_df_1['book_value_per_share'] = merged_df_1.groupby('stock_code')['book_value_per_share'].ffill()


# calculate P/E and P/B ratio
merged_df_1['P/E'] = merged_df_1['closing_price'] / merged_df_1['earnings_per_share']
# merged_df_1['P/E'] = merged_df_1['closing_price'] / merged_df_1['earnings_per_share'] / 3
merged_df_1['P/B'] = merged_df_1['closing_price'] / merged_df_1['book_value_per_share']


""" draw the time series of P/E ratios """

estDate_type = estDate_type.drop(columns=['Stknme_en'])
estDate_type = estDate_type.drop(columns=['Listdt'])
estDate_type = estDate_type.drop(columns=['Estbdt'])
estDate_type.columns = ['stock_code', 'market_type']

# merge merged_df_1 and estDate_type
merged_df_1 = pd.merge(merged_df_1, estDate_type, on=['stock_code'], how='left')


# convert "date" column to period type
merged_df_1['date'] = merged_df_1['date'].dt.to_timestamp()

# if market_type is 1, 4, 64, make them all main board
merged_df_1['market_type'] = merged_df_1['market_type'].replace([1, 4, 64], "Main Board")
merged_df_1['market_type'] = merged_df_1['market_type'].replace([16, 32], "GEM")


# 对 DataFrame 按照 'market_type' 分组，然后计算每个市场类型的 P/E 比率的中位数时间序列
pe_by_market_type = merged_df_1.groupby(['market_type', 'date'])['P/E'].median().unstack(level=0)
# pe_by_market_type.to_csv('pe_by_market_type.csv')


# summary statistics for main board
summary_df_mainBoard = merged_df_1[merged_df_1['market_type'] == 'Main Board'].describe()
summary_df_mainBoard = summary_df_mainBoard.round(2)
summary_df_mainBoard.to_csv('summary_df_1_mainBoard.csv')


# summary statistics for GEM
summary_df_GEM = merged_df_1[merged_df_1['market_type'] == 'GEM'].describe()
summary_df_GEM = summary_df_GEM.round(2)
summary_df_GEM.to_csv('summary_df_1_GEM.csv')


# 绘制两个市场类型的中位数 P/E 比率时间序列图表
pe_by_market_type.plot(figsize=(16, 7))
plt.title('Median P/E Ratio by Market Type')
plt.xlabel('Date')
plt.ylabel('Median P/E Ratio')
plt.grid(True)
plt.legend(title='Market Type')
plt.show()
