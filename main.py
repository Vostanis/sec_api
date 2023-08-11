from json_db import *

# import keyboard << come back to this

# Settings Parameters
daily_refresh_flag  = 0




### INIT STAGE BEGINS ###
#########################
clear_screen()
print("Deploying ...")

# Download bulk .zip of all SEC submission files and company facts
# # If the file already exists & is modified today: do not redownload
def refresh():
    if not os.path.exists(zip_dir):
        print(f"Installing directory: {zip_dir}")
        os.makedirs(zip_dir)

    if daily_refresh_flag == 1:
        print("Gateway 1 ...")
        cf_zip_path = zip_dir+"\\companyfacts.zip"

        if os.path.exists(cf_zip_path) and (datetime.date.fromtimestamp(os.path.getmtime(cf_zip_path)) == today): 
            print("Passing ...")
            pass
        else:
            print("Installing ...")
            load_url("https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip", dir=zip_dir)

        print("Gateway 2 ...")
        sbm_zip_path = zip_dir+"\\submissions.zip"

        if os.path.exists(sbm_zip_path) and (datetime.date.fromtimestamp(os.path.getmtime(sbm_zip_path)) == today): 
            print("Passing ...")
            pass
        else:
            print("Installing ...")
            load_url("https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip", dir=zip_dir)

        # Unzip the bulk data
        # Company Facts
        print("Gateway 3 ...")
        # cf_dir = home_dir+"\\companyfacts"
        if not os.path.exists(cf_dir):
            print(f"Installing directory: {cf_dir}")
            os.makedirs(cf_dir)
        if len(os.listdir(cf_dir)) == 0:
            unzip(cf_zip_path, cf_dir)
        if os.path.exists(cf_dir) and (datetime.date.fromtimestamp(os.path.getmtime(cf_dir)) != today):
            try:
                unzip(cf_zip_path, cf_dir)
            except Exception:
                print(".zip corrupted - redownloading .zip")
                os.remove(cf_zip_path)
                load_url("https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip", dir=zip_dir)
        else:
            print("Passing\t")
            pass
        
        # Submissions
        print("Gateway 4 ...")
        # sbms_dir = home_dir+"\\submissions"
        if not os.path.exists(sbms_dir):
            print(f"Installing directory: {sbms_dir}")
            os.makedirs(sbms_dir)

        if len(os.listdir(sbms_dir)) == 0:
            unzip(sbm_zip_path, sbms_dir)

        if os.path.exists(sbms_dir) and (datetime.date.fromtimestamp(os.path.getmtime(sbms_dir)) != today):
            try:
                unzip(sbm_zip_path, sbms_dir) # What if .zip corrupts?
            except Exception:
                print(".zip corrupted - redownloading .zip")
                os.remove(sbm_zip_path)
                load_url("https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip", dir=zip_dir)
                unzip(sbm_zip_path, sbms_dir)
            print("Passing\t..")
            pass

        # Download CIK Code, Ticker Symbol, Company Name from .json link and store as a .pkl file
        
        if not os.path.exists(tikr_dir):
            print(f"Installing directory: {tikr_dir}")
            os.makedirs(tikr_dir)
        print("Requesting data ...")
        tikrs = pd.DataFrame(load_url("https://www.sec.gov/files/company_tickers.json"))
        tikrs.to_pickle(tikr_dir + "\\tikrs.pkl")
    else:
        pass
refresh()

init_tikr = pd.read_pickle(tikr_dir+"\\tikrs.pkl")
tikrs = pd.DataFrame(init_tikr)
tikrs = tikrs.transpose()
tikrs['cik_str'] = tikrs['cik_str'].apply('{:0>10}'.format)
print("Deployment complete.")
clear_screen()
# <<< install permanent state of Ticker table

###########################
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

# Schema complete; all tables can now be joined    <<<   data traversal begins here
clear_screen()

sbms_json   = sbms_dir+"\\CIK"+cik_x+".json"
cf_json     = cf_dir  +"\\CIK"+cik_x+".json"

def submissions_or_facts():
    while True:
        print("SEC API >> TICKERS >> ...\n")
        print("Press 1 for all Reports & Submissions\nPress 2 for Company Data Overview\n")
        input_key = input().upper()
        if   input_key == '1':
            return pd.read_json(sbms_json)
        elif input_key == '2':
            return pd.read_json(cf_json)

current = submissions_or_facts()
current = pd.DataFrame(current["facts"][0])
print(current)
# print(pd.json_normalize(submissions_or_facts()))



























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