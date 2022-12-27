from urllib.request import urlopen
import requests
import json
import pandas as pd

class json_df:
    def __init__(self, url):
        # call disguised as Firefox browser
        self.request    = json.loads((requests.get(url, headers={"User-Agent": "Mozilla/5.0"})).text)
        self.df         = pd.json_normalize(self.request)

    def view_columns(self):
        print(self.df.columns.tolist())