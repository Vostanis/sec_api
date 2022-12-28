import matplotlib.pyplot as plt
from json_df import *


tikrs = json_df("https://www.sec.gov/files/company_tickers.json")
tikrs.df = tikrs.df.transpose()
# cik code is considered int, so fill up to 10th character with zeros (if necessary)
tikrs.df['cik_str'] = tikrs.df['cik_str'].apply('{:0>10}'.format)

# input ticker, locate respective index, and retrieve CIK code for joining
# print('ENTER TICKER SYMBOL:\t')
# tikr_x        = input().upper()
tikr_x          = 'JNJ' # test example
# retrieve index and CIK
cik_x = tikrs.find(tikr_x, 'ticker', 'cik_str')

# build dfs, of relevant company; joint on CIK
# filings     = json_df(f"https://data.sec.gov/submissions/CIK{cik_x}.json")
concepts    = json_df(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_x}/us-gaap/AccountsPayableCurrent.json")
facts       = json_df(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_x}.json")

# print(filings.df)
print(concepts.df)
print(facts.df)
# print(filings.df_normalized)
print(concepts.df_normalized)
print(facts.df_normalized)





cik_url         = f"https://data.sec.gov/submissions/CIK{cik_x}.json"
concepts_url    = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_x}/us-gaap/AccountsPayableCurrent.json"
facts_url       = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_x}.json"
# print(cik_url)
# print(concepts_url)
# print(facts_url)
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
eps_df_10q = eps_df.set_index('end').dropna()
# print(eps_df_10q)
# print(eps_df.dropna())
eps_df_10k = eps_df[(eps_df['frame'].str.len() == 8)].set_index('end').dropna()
# print(eps_df_10k)
# print(concepts_df['units.USD'][0])
# print(concepts_df['units.USD'][0][0])

# usd_df = pd.DataFrame(concepts_df['units.USD'][0])
# print(usd_df)
# print(usd_df.columns.tolist())

# shares_outstanding_df.plot(x='end', y='val', kind='line')
# plt.show()
# eps_df.plot(x='end', y='val', kind='line')
# plt.show()
# eps_df_10q.plot(x='end', y='val', kind='line')
# plt.show()
# eps_df_10k.plot(x='end', y='val', kind='line')
# plt.show()

# info screen
print(
     f"{cik_df['name'].values[0].upper()}\t\t\t\t\t{cik_df['entityType'].values[0].upper()}\n=================================================\n\n",
    f"EPS:\t\t\t\t\t\t\t\t{eps_df_10k['val'][eps_df_10k.index[-1]]}"
)