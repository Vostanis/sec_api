from urllib.request import urlopen
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

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
tikr_x          = 'AZPN' # test example
##################################

# 2. retrieve index and CIk
index_x         = tikr_df.index[tikr_df['ticker'] == tikr_x][0]
cik_x           = tikr_df.iloc[[index_x]]['cik_str'].values[0]
# print(index_x)
# print(cik_x)

# 3. build dfs, of relevant company, via CIK
cik_url         = f"https://data.sec.gov/submissions/CIK{cik_x}.json"
concepts_url    = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_x}/us-gaap/AccountsPayableCurrent.json"
facts_url       = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_x}.json"
print(cik_url)
print(concepts_url)
print(facts_url)
# send the request with a Firefox header (keeps it generalised; would need an email otherwise)
cik_response        = json.loads((requests.get(cik_url,         headers={"User-Agent": "Mozilla/5.0"})).text)
concepts_response   = json.loads((requests.get(concepts_url,    headers={"User-Agent": "Mozilla/5.0"})).text)
facts_response      = json.loads((requests.get(facts_url,       headers={"User-Agent": "Mozilla/5.0"})).text)
# print(concepts_response)
cik_df              = pd.json_normalize(cik_response)
concepts_df         = pd.json_normalize(concepts_response)
facts_df            = pd.json_normalize(facts_response)

# df playground
# print(cik_df.columns.tolist())
print(cik_df)
# filings_df = pd.DataFrame(cik_df['filings.files'][0])
# print(filings_df)
# print(concepts_df.columns.tolist())
print(facts_df.columns.tolist())
print(facts_df['facts.dei.EntityCommonStockSharesOutstanding.units.shares'][0])
shares_outstanding_df = pd.DataFrame(facts_df['facts.dei.EntityCommonStockSharesOutstanding.units.shares'][0])
print(shares_outstanding_df)
eps_df = pd.DataFrame(facts_df['facts.us-gaap.EarningsPerShareBasic.units.USD/shares'][0])
eps_df_filtered = eps_df[eps_df['form'] != '10-K'].dropna()
print(eps_df_filtered)
# print(concepts_df['units.USD'][0])
# print(concepts_df['units.USD'][0][0])
# usd_df = pd.DataFrame(concepts_df['units.USD'][0])
# print(usd_df)
# print(usd_df.columns.tolist())

shares_outstanding_df.plot(x='end', y='val', kind='line')
plt.show()
eps_df.plot(x='end', y='val', kind='line')
plt.show()
