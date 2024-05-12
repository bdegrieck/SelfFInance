import numpy as np
import pandas as pd

from BackEnd.error import InsufficientData


# tickers that the api cannot understand when inputting full company name instead of ticker
def check_raw_data(ticker_raw_data: dict) -> str:
    for raw_data_dict in ticker_raw_data:
        if not raw_data_dict:
            InsufficientData(f"Inputted ticker: {self.ticker} does not have enough data to display")


# cleans dataframe to remove nan values and 'None'
def get_clean_data(df_data: dict) -> dict:
    for data_category, df_value in df_data.items():
        for column in df_value.columns:
            df_data[data_category][column] = df_value[column].fillna(0).replace(to_replace="None", value=np.nan)
            try:
                df_data[data_category][column] = df_data[data_category][column].astype(float)
            except:
                pass
    return df_data


# removes rows of data that have 0 as date
def remove_empties(df_data: dict) -> dict:
    for data_category, df_value in df_data.items():
        df_data[data_category] = df_value[df_value.index.notna()]
    return df_data


def get_ticker_balance_df_adj(balance_df: pd.DataFrame) -> pd.DataFrame:
    balance_df["cashFlow"] = balance_df[["operatingCashFlow", "cashFlowFromFinancing", "cashFlowFromInvestment"]].sum(axis=1)
    return balance_df[["totalRevenue", "profit", "cashFlow", "reportedDate"]]


def get_technical_analysis_values(tech_analysis_dict: dict, tech_analysis_name: str):
    technical_analysis_values = []
    for date, tech_analysis_dict_values in tech_analysis_dict.items():
        technical_analysis_values.append(float(tech_analysis_dict_values[tech_analysis_name]))
    return technical_analysis_values


def get_bbands_technical_analysis_values(tech_analysis_dict: dict):
    lower_bound_data = []
    middle_bound_data = []
    upper_bound_data = []

    for date, bbands_values in tech_analysis_dict.items():
        lower_bound_data.append(bbands_values["Real Lower Band"])
        middle_bound_data.append(bbands_values["Real Middle Band"])
        upper_bound_data.append(bbands_values["Real Upper Band"])

    return {
        "lowerBound": lower_bound_data,
        "middleBound": middle_bound_data,
        "upperBound": upper_bound_data,
    }