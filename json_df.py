from urllib.request import urlopen
import requests
import json
import pandas as pd
import polars as pl


class json_df:
    def __init__(self, url=None, txt=None):
        if url is not None:
            # call disguised as a Firefox browser
            self.request = json.loads((requests.get(url, headers={"User-Agent": "Mozilla/5.0"})).text)
        if txt is not None:
            self.request = json.loads(txt)
        # if txt is not None and url is not None:
        #     print('\033[1;31mInputError: input requires only one parameter\n\033[0m')

        try:
            self.df             = pd.DataFrame(self.request)
            self.df_normalized  = pd.json_normalize(self.request)
        except ValueError:
            self.df             = pd.json_normalize(self.request)
            self.df_normalized  = self.df
            print(f'\033[1;31mValueError for {self}: {__name__} must use normalized format instead\n\033[0m')


    # quick view of entire df
    def view_columns(self):
        print(self.df_normalized.columns.tolist())

    # index match (input & input column : output column & output)
    def find(self, input_x, in_col, out_col):
        input_index = self.df.index[self.df[in_col] == input_x][0]
        return self.df.iloc[[input_index]][out_col].values[0]

    # unpack nested JSON into df
    def unpack(self, col_name):
        return pd.DataFrame(self.df_normalized[col_name][0])

    # limit df to last y values
    def limit(self, y=10):
        return self.df.tail(y)