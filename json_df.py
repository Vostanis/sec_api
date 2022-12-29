from urllib.request import urlopen
import requests
import json
import pandas as pd

################################################ INIT. FUNCTIONS ######################################################

# call .json url, default disguised as a Firefox browser
def json_url(url, user_agent="Mozilla/5.0"):
    return json.loads((requests.get(url, headers={"User-Agent": user_agent})).text)

# json zip ?
# json html ?

#######################################################################################################################

class json_df:
    def __init__(self, df):
        try:
            self.df = pd.DataFrame(df)
        except ValueError:
            self.df = pd.json_normalize(df)
            print(f'\033[1;31mValueError for {self}: {__name__} normalized instead\n\033[0m')

        self.df_normalized = pd.json_normalize(df)

    # quick view of entire df
    def view_columns(self):
        print(self.df_normalized.columns.tolist())

    # index match (input & input column : output column & output)
    def find(self, input_x, in_col, out_col):
        input_index = self.df.index[self.df[in_col] == input_x][0]
        return self.df.iloc[[input_index]][out_col].values[0]

    # unpack nested JSON into df
    def unpack(self, col_name):
        return json_df(self.df_normalized[col_name][0])