import pandas as pd


# merges two dfs on index
def merge(df1: pd.DataFrame, df2: pd.DataFrame):
    return pd.merge(df1, df2, left_index=True, right_index=True)


# calculates difference percentage between two series from series 2 to series 1
def get_series_difference_percentage(series1: pd.Series, series2: pd.Series) -> pd.Series:
    calculated_difference = ((series2 - series1) / series1) * 100
    return calculated_difference


# shifts df columns to -1 for down or 1 for up and gets the difference
def get_shifted_differences(df: pd.DataFrame, columns_to_shift: list, shift_motion: int = -1):
    for column in columns_to_shift:
        df[f"{column}Difference"] = df[column] - df[column].shift(shift_motion)
    return df
