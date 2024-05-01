import numpy as np
import pandas as pd
import requests

from BackEnd import constants
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
            df_data[data_category][column] = df_value[column].fillna(0).replace(to_replace=["None", np.nan], value=0)
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


class API:

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ticker_endpoints = self.get_endpoint_company()
        self.ticker_raw_data = self.get_raw_api_data(endpoints=self.ticker_endpoints)
        self.ticker_df_data = self.get_company_df_data()

    # format company endpoints
    def get_endpoint_company(self) -> dict:
        dict_functions_company_urls = {
            "times_series_data": f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&apikey={constants.API_KEY}&outputsize=full",
            "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={constants.API_KEY}",
            "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.ticker}&apikey={constants.API_KEY}",
            "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.ticker}&apikey={constants.API_KEY}",
            "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.ticker}&apikey={constants.API_KEY}",
            "earnings": f"https://www.alphavantage.co/query?function=EARNINGS&symbol={self.ticker}&apikey={constants.API_KEY}"
        }

        return dict_functions_company_urls

    # get raw data endpoints are passed in
    def get_raw_api_data(self, endpoints: dict) -> dict:
        raw_data = {}
        for data_description, endpoint_url in endpoints.items():
            raw_data[data_description] = requests.get(url=endpoint_url).json()
        check_raw_data(ticker_raw_data=raw_data)
        return raw_data

    # format raw data to specific data returns a dictionary of dfs
    def get_company_df_data(self) -> dict:
        company_dfs = {}

        company_dfs["ticker_prices_df"] = pd.DataFrame(self.ticker_raw_data["times_series_data"]["Time Series (Daily)"]).transpose()
        company_dfs["ticker_prices_df"].columns = ["open", "high", "low", "adjustedClose", "close", "volume", "dividends", "splits"]
        company_dfs["ticker_prices_df"] = company_dfs["ticker_prices_df"][["open", "high", "low", "close", "volume"]]
        company_dfs["ticker_prices_df"].index = pd.DatetimeIndex(company_dfs["ticker_prices_df"].index)

        company_dfs["ticker_overview_df"] = pd.DataFrame({
            "tickerSymbol": [self.ticker_raw_data["overview"]["Symbol"]],
            "companyDescription": self.ticker_raw_data["overview"]["Description"],
            "marketCap": self.ticker_raw_data["overview"]["MarketCapitalization"],
            "52weekHigh": self.ticker_raw_data["overview"]["52WeekHigh"],
            "52weekLow": self.ticker_raw_data["overview"]["52WeekLow"]
        })

        company_dfs["ticker_eps_df"] = pd.DataFrame(self.ticker_raw_data["earnings"]["quarterlyEarnings"]).set_index("fiscalDateEnding")[["estimatedEPS", "reportedEPS", "surprisePercentage", "reportedDate"]]
        company_dfs["ticker_eps_df"].index = pd.DatetimeIndex(company_dfs["ticker_eps_df"].index)

        company_dfs["ticker_balance_df"] = pd.DataFrame({
            "date": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["fiscalDateEnding"],
            "totalRevenue": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["totalRevenue"],
            "profit": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["netIncome"],
            "operatingCashFlow": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["operatingCashflow"],
            "cashFlowFromFinancing": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromFinancing"],
            "cashFlowFromInvestment": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromInvestment"],
            "reportedDate": pd.DataFrame(self.ticker_raw_data["earnings"]["quarterlyEarnings"])["reportedDate"]
        }).set_index("date")

        company_dfs["ticker_balance_df"].index = pd.DatetimeIndex(company_dfs["ticker_balance_df"].index)

        # data cleanse
        company_dfs = get_clean_data(company_dfs)
        company_dfs = remove_empties(company_dfs)

        company_dfs["ticker_balance_df"] = get_ticker_balance_df_adj(company_dfs["ticker_balance_df"])

        return company_dfs
