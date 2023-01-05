import matplotlib.pyplot as plt
from json_df import *


tikrs      = json_df(url="https://www.sec.gov/files/company_tickers.json")
tikrs.df   = tikrs.df.transpose()
tikrs.df['cik_str'] = tikrs.df['cik_str'].apply('{:0>10}'.format) # fill loose CIK no.s with 0 (10 char length)

# input ticker, locate respective index, and retrieve CIK code for joining
# print('ENTER TICKER SYMBOL:\t')
# tikr_x    = input().upper()
tikr_x      = 'TMUS' # test example

# retrieve index and CIK
cik_x       = tikrs.find(tikr_x, 'ticker', 'cik_str')

# build dfs, of relevant company; joint on CIK
filings     = json_df(url=f"https://data.sec.gov/submissions/CIK{cik_x}.json")
# concepts    = json_df(url=f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_x}/us-gaap/AccountsPayableCurrent.json")
facts       = json_df(url=f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_x}.json")

# shares outstanding example case
sharesOutstanding = json_df(nest=facts.df_normalized['facts.dei.EntityCommonStockSharesOutstanding.units.shares'])
sharesOutstanding.df = sharesOutstanding.df.dropna().tail(15)
sharesOutstanding.df.plot(x='end', y='val', kind='line')
plt.show()

eps = json_df(nest=facts.df_normalized['facts.us-gaap.EarningsPerShareBasic.units.USD/shares'])
print(eps.df.dropna().tail(15))

# info screen
# print(
#      f"{cik_df['name'].values[0].upper()}\t\t\t\t\t{cik_df['entityType'].values[0].upper()}\n=================================================\n\n",
#     f"EPS:\t\t\t\t\t\t\t\t{eps_df_10k['val'][eps_df_10k.index[-1]]}"
# )