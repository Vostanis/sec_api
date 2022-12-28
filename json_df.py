from urllib.request import urlopen
import requests
import json
import pandas as pd
import numpy as np


class json_df:
    def __init__(self, url):
        # call disguised as a Firefox browser
        self.request = json.loads((requests.get(url, headers={"User-Agent": "Mozilla/5.0"})).text)
        self.df = pd.DataFrame(self.request)
        self.df_normalized = pd.json_normalize(self.request)

    # quick view of entire df
    def view_columns(self):
        print(self.df_normalized.columns.tolist())

    def find(self, input_x, in_col, out_col):
        input_index = self.df.index[self.df[in_col] == input_x][0]
        return self.df.iloc[[input_index]][out_col].values[0]