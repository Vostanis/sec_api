from df_shortcuts import *
from functions import *

# import keyboard << come back to this





### INIT STAGE BEGINS ###
clear_screen()
print("Deploying ...")
# Download bulk .zip of all SEC submission files and company facts
# # If the file already exists & is modified today: do not redownload
print("Gateway 1 ...")
cf_file_path = zip_dir+"\\companyfacts.zip"
download_gateway(cf_file_path,  load_url("https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip", dir=zip_dir))
print("Gateway 2 ...")
sbm_file_path = zip_dir+"\\submissions.zip"
download_gateway(sbm_file_path, load_url("https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip", dir=zip_dir))

# Unzip the bulk data
print("Gateway 3 ...")
if os.path.exists(db_dir+"\\companyfacts") and (datetime.date.fromtimestamp(db_dir + "\\companyfacts") == today):
    pass
else:
    print("Unpacking companyfacts.zip ...")
    unzip(zip_dir+"\\companyfacts.zip", db_dir)
print("Gateway 4 ...")
if os.path.exists(db_dir+"\\submissions") and (datetime.date.fromtimestamp(db_dir + "\\submissions") == today):
    pass
else:
    print("Unpacking submissions.zip ...")
    unzip(zip_dir+"\\submissions.zip", db_dir)

# Download CIK Code, Ticker Symbol, Company Name from .json link
print("Requesting data ...")
tikrs = json_df(load_url("https://www.sec.gov/files/company_tickers.json"))
tikrs.df = tikrs.df.transpose()
tikrs.df['cik_str'] = tikrs.df['cik_str'].apply('{:0>10}'.format)
print("Deployment complete.")
clear_screen()
### INIT STAGE COMPLETE ###





### USER STAGE BEGINS ###
print("SEC API >> ...\n")

# input ticker, locate respective index, and retrieve CIK code for joining
def input_tikr():
    print("Enter Ticker Symbol:\t")
    input_ticker = input().upper()
    try:
        output_cik = tikrs.find(input_ticker, 'ticker', 'cik_str')
    except IndexError:
        # find all tickers with same first 2 symbols for suggestions
        matching_tickers = []
        for ticker, company_name in zip(tikrs.df['ticker'], tikrs.df['title']):
            if ticker[:2] == input_ticker[:2]:
                matching_tickers.append((ticker, company_name))
        
        # (number_of_suggestions > 0) => print them
        if len(matching_tickers) != 0:
            clear_screen()
            print("SEC API >> ...\n")
            print(f"{input_ticker} does not exist, please try again. Here are some suggestions, based on your input:")
            for ticker, company_name in matching_tickers:
                print(f"\t{ticker}\t\t{company_name}")
            print()
            return input_tikr()
        
        # (number_of_suggestions = 0)
        else:
            print(f"\n{input_ticker} does not exist, please try another Ticker Symbol.\n")
            return input_tikr()
    
    return output_cik

cik_x = input_tikr()
# print(cik_x)

# Schema complete; data traversal begins here
clear_screen()

submissions_zip = "submissions.zip"
# submissions_zip = home_dir + "\\submissions.zip"
# submissions_json = home_dir + "\\submissions\\CIK" + cik_x + ".json"
submissions_json = "CIK" + cik_x + ".json"

companyfacts_zip = "companyfacts.zip"
# companyfacts_json = home_dir + "\\companyfacts\\CIK" + cik_x + ".json"
companyfacts_json = "CIK" + cik_x + ".json"
print(submissions_zip)
print(submissions_json)
print(companyfacts_zip)
print(companyfacts_json)

def submissions_or_facts():
    print("SEC API >> TICKERS >> ...\n")
    print("1. Report Submissions, enter 'S'\n2. Company Data, enter 'D'\n")
    input_key = input().upper()
    if input_key == 'S':
        return json_df(load_compr_file(submissions_zip, submissions_json))
    elif input_key == 'D':
        return json_df(load_compr_file(companyfacts_zip, companyfacts_json))
    else:
        submissions_or_facts()

current = submissions_or_facts()
print(current.df)








































































# build dfs, of relevant company; joint on CIK
# filings         = json_df(load_url(f"https://data.sec.gov/submissions/CIK{cik_x}.json"))
# concepts        = json_df(load_url(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_x}/us-gaap/AccountsPayableCurrent.json"))
# facts           = json_df(load_url(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_x}.json"))

# print(filings.df_normalized)
# print(concepts.df)
# print(concepts.df_normalized)
# print(facts.df)
# print(concepts.df_normalized)
# print(facts.df_normalized)
# print(facts.df_normalized['facts.us-gaap.EarningsPerShareBasic.units.USD/shares'])
# print(facts.df_normalized['facts.us-gaap.EarningsPerShareBasic.units.USD/shares'][0])
# eps_df = pd.DataFrame(facts.df_normalized['facts.us-gaap.EarningsPerShareBasic.units.USD/shares'])
# print(eps_df)
# print(facts.df_normalized)
# print(filings.df_normalized)
# eps_df = pd.DataFrame(facts.df_normalized['facts.us-gaap.EarningsPerShareBasic.units.USD/shares'][0])
# print(eps_df)
# eps         = json_df(facts.unpack('facts.us-gaap.EarningsPerShareBasic.units.USD/shares'))
# print(eps.df)


# cik_url         = f"https://data.sec.gov/submissions/CIK{cik_x}.json"
# concepts_url    = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_x}/us-gaap/AccountsPayableCurrent.json"
# facts_url       = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_x}.json"
# print(cik_url)


# print(concepts_url)
# print(facts_url)
# send the request with a Firefox header (keeps it generalised; would need an email otherwise)
# cik_response        = json.loads((requests.get(cik_url,         headers={"User-Agent": "Mozilla/5.0"})).text)
# concepts_response   = json.loads((requests.get(concepts_url,    headers={"User-Agent": "Mozilla/5.0"})).text)
# facts_response      = json.loads((requests.get(facts_url,       headers={"User-Agent": "Mozilla/5.0"})).text)
# print(concepts_response)
# cik_df              = pd.json_normalize(cik_response)
# concepts_df         = pd.json_normalize(concepts_response)
# facts_df            = pd.json_normalize(facts_response)

# df playground
# print(cik_df.columns.tolist())
# print(cik_df)
# filings_df = pd.DataFrame(cik_df['filings.files'][0])
# print(filings_df)
# print(concepts_df.columns.tolist())
# print(facts_df.columns.tolist())
# print(facts_df['facts.dei.EntityCommonStockSharesOutstanding.units.shares'][0])
# shares_outstanding_df = pd.DataFrame(facts_df['facts.dei.EntityCommonStockSharesOutstanding.units.shares'][0])
# print(shares_outstanding_df)
# eps_df = pd.DataFrame(facts_df['facts.us-gaap.EarningsPerShareBasic.units.USD/shares'][0])
# eps_df_10q = eps_df.set_index('end').dropna()
# print(eps_df_10q)
# print(eps_df.dropna())
# eps_df_10k = eps_df[(eps_df['frame'].str.len() == 8)].set_index('end').dropna()
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
# print(
#      f"{cik_df['name'].values[0].upper()}\t\t\t\t\t{cik_df['entityType'].values[0].upper()}\n=================================================\n\n",
#     f"EPS:\t\t\t\t\t\t\t\t{eps_df_10k['val'][eps_df_10k.index[-1]]}"
# )