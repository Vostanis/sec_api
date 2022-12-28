from urllib.request import urlopen
import requests
import json
import pandas as pd
import numpy as np


class json_df:
    def __init__(self, url, x):
        # call disguised as Firefox browser
        self.request = json.loads((requests.get(url, headers={"User-Agent": "Mozilla/5.0"})).text)
        self.df = pd.DataFrame(self.request)
        self.df_normalized = pd.json_normalize(self.request)
        self.connector = x

    # quick view of entire df
    def view_columns(self):
        print(self.df_normalized.columns.tolist())

    # set connector for joins
    def connector(self, x):
        self.connector = x