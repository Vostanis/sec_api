import pandas as pd

class json_df:
    def __init__(self, df):
        try:
            self.df = pd.DataFrame(df)
        except ValueError:
        # self.df = pd.json_normalize(df)
            print(f'\033[1;31mValueError for {self}; consider using normalized equivalent\n\033[0m')

        try:
            self.df_normalized = pd.json_normalize(df)
        except NotImplementedError:
            print(f'\033[1;31mNotImplementedError for {self}: {__name__} cannot be normalized\n\033[0m')

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