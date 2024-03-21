import numpy as np
import requests

from BackEnd.data import get_html, get_raw_api_data, get_clean_data, remove_empties
import pandas as pd
from BackEnd import constants


class CompanyData:

    def __init__(self, ticker: str):
        self.api_key = constants.API_KEY
        self.ticker = ticker
        self.ticker_endpoints = self.get_endpoint_company()
        self.ticker_raw_data = get_raw_api_data(endpoints=self.ticker_endpoints)
        self.ticker_df_data = self.get_company_df_data()
        self.ticker_html_data = get_html(df_data=self.ticker_df_data)

    # format company endpoints
    def get_endpoint_company(self) -> dict:
        dict_functions_company_urls = {
            "times_series_data": f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&apikey={self.api_key}&outputsize=full",
            "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={self.api_key}",
            "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.ticker}&apikey={self.api_key}",
            "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.ticker}&apikey={self.api_key}",
            "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.ticker}&apikey={self.api_key}",
            "earnings": f"https://www.alphavantage.co/query?function=EARNINGS&symbol={self.ticker}&apikey={self.api_key}"
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

        company_dfs = get_clean_data(company_dfs)
        company_dfs = remove_empties(company_dfs)

        company_dfs["ticker_balance_df"] = self.get_ticker_balance_df_adj(company_dfs["ticker_balance_df"])
        return company_dfs

    def get_ticker_balance_df_adj(self, balance_df: pd.DataFrame) -> pd.DataFrame:
        balance_df["Cash Flow"] = balance_df[["Operating Cash Flow", "Cash Flow From Financing", "Cash Flow From Investment"]].sum(axis=1)
        return balance_df[["Total Revenue", "Profit", "Cash Flow"]]
