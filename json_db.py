import pandas as pd

class json_df:
    def __init__(self, df):

        # 1st try to load .json file
        try:
            self.df = pd.read_json(df)
        except Exception:
            pass

        # Then try a normale Pandas DataFrame
        try:
            self.df = pd.DataFrame(df)
        except ValueError:
            self.df = "ERROR: DataFrame is not available."

        # Try a normalized option
        try:
            self.df_normalized = pd.json_normalize(df)
        except NotImplementedError:
            self.df_normalized = "ERROR: Normalized DataFrame is not available."

        
    # quick view of entire df by its columns
    def print_col(self):
        print(self.df_normalized.columns.tolist())

    # index match (input & input column : output column & output)
    def find(self, input_x, in_col, out_col):
        input_index = self.df.index[self.df[in_col] == input_x][0]
        return self.df.iloc[[input_index]][out_col].values[0]

    # unpack nested json into df
    def unpack(self, col_name):
        return json_df(self.df_normalized[col_name][0].to_json())