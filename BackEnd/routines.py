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


def find_closest_dates_before(date, data_df):
    return data_df[data_df.index < date].first_valid_index()


def find_closest_dates_after(date, data_df):
    return data_df[data_df.index > date].last_valid_index()


def get_techincal_indicator_earnings(df: pd.DataFrame, report_dates: dict, column_name: str) -> dict:
    sma_earnings = {}
    report_dates = {quarter_date: report_date for quarter_date, report_date in report_dates.items() if report_date > df.index[-1]}
    for quarter_date, report_date in report_dates.items():
        if df[df.index == report_date].empty:
            closest_date = find_closest_dates_before(data_df=df, date=report_date)
            sma_earnings[quarter_date] = df[df.index == closest_date][column_name].iloc[0]
        else:
            sma_earnings[quarter_date] = df[df.index == report_date][column_name].iloc[0]
    return sma_earnings
