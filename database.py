from urllib.request import urlopen
import json
import pandas as pd
import requests

# tikr set
tikr_url = "https://www.sec.gov/files/company_tickers.json"
tikr_response = urlopen(tikr_url)
tikr_df = pd.DataFrame(json.loads(tikr_response.read())).transpose()

# cik code is considered int, so fill up to 10th character with zeros if necessary
tikr_df['cik_str'] = tikr_df['cik_str'].apply('{:0>10}'.format)
# print(tikr_df)

# input ticker, locate respective index, and retrieve CIK code for joining
print('Enter Ticker Symbol:\t')
tikr_x = input().upper()
print(tikr_df.loc[tikr_df['ticker'] == tikr_x])
index_x = tikr_df.index[tikr_df['ticker'] == tikr_x][0]
cik_x = tikr_df.iloc[[index_x]]['cik_str'].values[0]
# print(index_x)
# print(cik_x)

# Maybe 3am JSON download setup (looking more likely; think SEC api would need company)
# Structure might be flawed as independent
# anywhere to virtually host this?? shouldn't be much data to download

# build submissions of selected ticker
cik_url = f"https://data.sec.gov/submissions/CIK{cik_x}.json"
# print(cik_url)
# send the request with Firefox header; assume Mozilla isn't designed for bots?
cik_response = json.loads((requests.get(cik_url, headers={"User-Agent": "Mozilla/5.0"})).text)
# cik_df = pd.read_json(cik_response)
print(cik_response)
cik_df = pd.DataFrame(json.normalize(cik_response))
