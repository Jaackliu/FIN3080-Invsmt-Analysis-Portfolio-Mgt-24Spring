
import pandas as pd


""" read files and basic data cleaning """


price_value_return = pd.read_csv('data/Monthly Return/TRD_Mnth.csv')
EPS_bookValue = pd.read_csv('data/Index per Share/FI_T9.csv')
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


""" derive quarterly R&D expense/total asset ratios and quarterly firm ages """

# rename columns
RnD = RnD.drop(columns=['ShortName_EN'])
RnD.columns = ['stock_code', 'date', 'R&D_expense']
asset_liability = asset_liability.drop(columns=['ShortName_EN'])
asset_liability.columns = ['stock_code', 'date', 'total_asset', 'total_liability']
estDate_type = estDate_type.drop(columns=['Stknme_en'])
estDate_type = estDate_type.drop(columns=['Listdt'])
estDate_type.columns = ['stock_code', 'est_date', 'market_type']
ROA_ROE = ROA_ROE.drop(columns=['ShortName_EN'])
ROA_ROE.columns = ['stock_code', 'date', 'ROA', 'ROE']


# convert "date" column to period type
RnD['date'] = pd.to_datetime(RnD['date']).dt.to_period('Q')
asset_liability['date'] = pd.to_datetime(asset_liability['date']).dt.to_period('Q')
estDate_type['est_date'] = pd.to_datetime(estDate_type['est_date']).dt.to_period('D')
quarter_list['date'] = pd.to_datetime(quarter_list['date']).dt.to_period('Q')
ROA_ROE['date'] = pd.to_datetime(ROA_ROE['date']).dt.to_period('Q')


# merge RnD and asset_liability and estDate_type on stock_code and date
merged_df_2 = pd.merge(quarter_list, asset_liability, on=['date'], how='left')
merged_df_2 = pd.merge(merged_df_2, RnD, on=['stock_code', 'date'], how='left')
merged_df_2 = pd.merge(merged_df_2, estDate_type, on=['stock_code'], how='left')
merged_df_2 = pd.merge(merged_df_2, ROA_ROE, on=['stock_code', 'date'], how='left')

# calculate R&D expense/total asset ratio
merged_df_2['R&D/asset'] = merged_df_2['R&D_expense'] / merged_df_2['total_asset']


""" derive firm ages """

# convert "date" column to string type
merged_df_2['date'] = merged_df_2['date'].astype(str)


def date_calculator(row):
    if row[-2:] == 'Q1':
        return row[:4] + '-03-31'
    elif row[-2:] == 'Q2':
        return row[:4] + '-06-30'
    elif row[-2:] == 'Q3':
        return row[:4] + '-09-30'
    else:
        return row[:4] + '-12-31'


merged_df_2['date_cal'] = merged_df_2['date'].apply(date_calculator)

merged_df_2['date_cal'] = pd.to_datetime(merged_df_2['date_cal'])
merged_df_2['est_date'] = merged_df_2['est_date'].dt.to_timestamp()
merged_df_2['firm_age'] = (merged_df_2['date_cal'] - merged_df_2['est_date']).dt.days / 365
merged_df_2 = merged_df_2.drop(columns=['date_cal'])



# classify the companies
# if market_type is 1, 4, 64, make them all main board
merged_df_2['market_type'] = merged_df_2['market_type'].replace([1, 4, 64], "Main Board")
merged_df_2['market_type'] = merged_df_2['market_type'].replace([16, 32], "GEM")


# summary statistics for main board
main_board = merged_df_2[merged_df_2['market_type'] == "Main Board"]
summary_df_2_mainBoard = main_board.describe()
summary_df_2_mainBoard = summary_df_2_mainBoard.round(2)
summary_df_2_mainBoard.to_csv('summary_df_2_mainBoard.csv')

# summary statistics for GEM
GEM = merged_df_2[merged_df_2['market_type'] == "GEM"]
summary_df_2_GEM = GEM.describe()
summary_df_2_GEM = summary_df_2_GEM.round(2)
summary_df_2_GEM.to_csv('summary_df_2_GEM.csv')
