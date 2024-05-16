import pandas as pd


# merges two dfs on index
def merge(df1: pd.DataFrame, df2: pd.DataFrame):
    return pd.merge(df1, df2, left_index=True, right_index=True)
