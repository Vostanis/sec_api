from urllib.request import urlopen
import json
import pandas as pd
import time

# tikr set
tikr_url = "https://www.sec.gov/files/company_tickers.json"
tikr_response = urlopen(tikr_url)
tikr_df = pd.DataFrame(json.loads(tikr_response.read())).transpose()

# cik code is considered int, so fill up to 10th character with zeros if necessary
tikr_df['cik_str'] = tikr_df['cik_str'].apply('{:0>10}'.format)

print(tikr_df)

print('Enter Ticker Symbol:\t')

tikr_x = input().upper()
print(tikr_df.loc[tikr_df['ticker'] == tikr_x])

index_x = tikr_df.index[tikr_df['ticker'] == tikr_x][0]
cik_x = tikr_df.iloc[[index_x]]['cik_str'].values[0]

print(index_x)
print(cik_x)

# time.sleep(4)
# need user-agent setup as below
#User-Agent:
# Sample Company Name AdminContact@<sample company domain>.com
# Accept-Encoding:
# gzip, deflate
# Host:
# www.sec.gov

# OR 3am JSON download setup (looking more likely; think SEC api would need company)
# maybe can't be done as independent
# anywhere to virtually host this?? shouldn't be much data to download

cik_url = f"https://data.sec.gov/submissions/CIK{cik_x}.json"
print(cik_url)
cik_response = urlopen(cik_url)
cik_df = pd.DataFrame(json.loads(cik_response.read())).transpose()

print(cik_df)
