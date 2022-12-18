from urllib.request import urlopen
import json
import pandas as pd
import requests

# tikr df
tikr_url        = "https://www.sec.gov/files/company_tickers.json"
tikr_response   = urlopen(tikr_url)
tikr_df         = pd.DataFrame(json.loads(tikr_response.read())).transpose()

# cik code is considered int, so fill up to 10th character with zeros if necessary
tikr_df['cik_str'] = tikr_df['cik_str'].apply('{:0>10}'.format)

# input ticker, locate respective index, and retrieve CIK code for joining
# 1. input ticker
##################################
# print('Enter Ticker Symbol:\t')
# tikr_x        = input().upper()
tikr_x          = 'JNJ'
##################################

# 2. retrieve index and CIk
index_x         = tikr_df.index[tikr_df['ticker'] == tikr_x][0]
cik_x           = tikr_df.iloc[[index_x]]['cik_str'].values[0]
print(index_x)
print(cik_x)

# 3. build dfs, of relevant company, via CIK
cik_url         = f"https://data.sec.gov/submissions/CIK{cik_x}.json"
concepts_url    = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_x}/us-gaap/AccountsPayableCurrent.json"
facts_url       = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_x}.json"
print(facts_url)

# send the request with a Firefox header (keeps it generalised; would need an email otherwise)
cik_df          = pd.json_normalize(json.loads((requests.get(cik_url,       headers={"User-Agent": "Mozilla/5.0"})).text))
concepts_df     = pd.json_normalize(json.loads((requests.get(concepts_url,  headers={"User-Agent": "Mozilla/5.0"})).text))
facts_df        = pd.json_normalize(json.loads((requests.get(facts_url,     headers={"User-Agent": "Mozilla/5.0"})).text))

# cik_df = pd.read_json(cik_response)
print(cik_df.columns.tolist())
print(concepts_df.columns.tolist())
print(facts_df.columns.tolist())
# pd.reset_option('max_columns')
print(cik_df['filings.recent.acceptanceDateTime'].values[0])
print(cik_df['filings.recent.form'].values[0])
# filings_df = pd.DataFrame(json.loads(cik_df['filings.files'].values[0]))
# print(filings_df)
# filings_df = json.loads(cik_df['filings.files'].text)
# print(filings_df.columns.tolist())

# print(cik_df)
# cik_df = pd.DataFrame(json_normalize(cik_response))
