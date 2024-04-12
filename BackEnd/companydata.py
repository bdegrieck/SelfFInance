import numpy as np
import pandas as pd

from BackEnd import constants
from BackEnd.api import API


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
    balance_df["Cash Flow"] = balance_df[["Operating Cash Flow", "Cash Flow From Financing", "Cash Flow From Investment"]].sum(axis=1)
    return balance_df[["Total Revenue", "Profit", "Cash Flow"]]


class CompanyData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ticker_endpoints = self.get_endpoint_company()
        self.ticker_raw_data = API(endpoints=self.ticker_endpoints, ticker=self.ticker).raw_data
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

    # format raw data to specific data returns a dictionary of dfs
    def get_company_df_data(self) -> dict:
        company_dfs = {}

        company_dfs["ticker_prices_df"] = pd.DataFrame(self.ticker_raw_data["times_series_data"]["Time Series (Daily)"]).transpose()
        company_dfs["ticker_prices_df"].columns = ["Open", "High", "Low", "Adjusted Close", "Close", "Volume", "Dividends", "Splits"]
        company_dfs["ticker_prices_df"] = company_dfs["ticker_prices_df"][["Open", "High", "Low", "Close", "Volume"]]

        company_dfs["ticker_overview_df"] = pd.DataFrame({
            "Ticker Symbol": [self.ticker_raw_data["overview"]["Symbol"]],
            "Company Description": self.ticker_raw_data["overview"]["Description"],
            "Market Cap": self.ticker_raw_data["overview"]["MarketCapitalization"],
            "52 Week High": self.ticker_raw_data["overview"]["52WeekHigh"],
            "52 Week Low": self.ticker_raw_data["overview"]["52WeekLow"]
        })

        company_dfs["ticker_eps_df"] = pd.DataFrame(self.ticker_raw_data["earnings"]["quarterlyEarnings"]).set_index("fiscalDateEnding")[["estimatedEPS", "reportedEPS", "surprisePercentage"]]

        company_dfs["ticker_balance_df"] = pd.DataFrame({
            "Date": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["fiscalDateEnding"],
            "Total Revenue": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["totalRevenue"],
            "Profit": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["netIncome"],
            "Operating Cash Flow": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["operatingCashflow"],
            "Cash Flow From Financing": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromFinancing"],
            "Cash Flow From Investment": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromInvestment"]
        }).set_index("Date")

        # data cleanse
        company_dfs = get_clean_data(company_dfs)
        company_dfs = remove_empties(company_dfs)

        company_dfs["ticker_balance_df"] = get_ticker_balance_df_adj(company_dfs["ticker_balance_df"])

        return company_dfs
