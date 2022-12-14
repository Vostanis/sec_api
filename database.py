from urllib.request import urlopen
import json
import pandas as pd

#
url = "https://www.sec.gov/files/company_tickers.json"
response = urlopen(url)
tikr_df = pd.DataFrame(json.loads(response.read())).transpose()

print(tikr_df)

print('Enter Ticker Symbol:\t')
tikr_x = input().upper()
print(tikr_df.loc[tikr_df['ticker'] == tikr_x])

cik_x = tikr_df.loc[tikr_df['cik_str'], 'ticker' == tikr_x].iloc[0]

print(cik_x)