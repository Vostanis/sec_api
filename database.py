from urllib.request import urlopen
import json
import pandas as pd

# tikr set
tikr_url = "https://www.sec.gov/files/company_tickers.json"
tikr_response = urlopen(tikr_url)
tikr_df = pd.DataFrame(json.loads(tikr_response.read())).transpose()

print(tikr_df)

print('Enter Ticker Symbol:\t')

tikr_x = input().upper()
print(tikr_df.loc[tikr_df['ticker'] == tikr_x])

index_x = tikr_df.index[tikr_df['ticker'] == tikr_x][0]
cik_x = tikr_df.iloc[[index_x]]['cik_str'].values[0]

print(index_x)
print(cik_x)
# cik_x = tikr_df.iloc[0][tikr_df['ticker'] == tikr_x]
# print(cik_x)
#
cik_url = f"https://data.sec.gov/submissions/CIK{cik_x}.json"
print(cik_url)
cik_response = urlopen(cik_url)
cik_df = pd.DataFrame(json.loads(cik_response.read())).transpose()

print(cik_df)