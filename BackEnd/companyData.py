from BackEnd.data import get_raw_api_data, get_html
from BackEnd.display import Display
import pandas as pd


class CompanyData:

    def __init__(self, ticker: str, api_key: str):
        self.ticker = ticker
        self.api_key = api_key
        self.ticker_endpoints = self.get_endpoint_company()
        self.ticker_raw_data = get_raw_api_data(endpoints=self.ticker_endpoints)
        self.ticker_df_data = self.get_company_df_data()
        self.ticker_html_data = get_html(df_data=self.ticker_df_data)
        #Display(html_data=self.ticker_html_data)

    # format company endpoints
    def get_endpoint_company(self) -> dict:
        dict_functions_company_urls = {
            "times_series_data": f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.ticker}&apikey={self.api_key}",
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
        company_dfs["ticker_overview_df"] = pd.DataFrame({
            "Ticker Symbol": [self.ticker_raw_data["overview"]["Symbol"]],
            "Company Description": [self.ticker_raw_data["overview"]["Description"]],
            "Market Cap": [self.ticker_raw_data["overview"]["MarketCapitalization"]],
            "52 Week High": [self.ticker_raw_data["overview"]["52WeekHigh"]],
            "52 Week Low": [self.ticker_raw_data["overview"]["52WeekLow"]]
        })
        company_dfs["ticker_eps_df"] = pd.DataFrame(self.ticker_raw_data["earnings"]["quarterlyEarnings"])
        company_dfs["ticker_balance_df"] = pd.DataFrame({
            "Date": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["fiscalDateEnding"],
            "Total Revenue": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["totalRevenue"],
            "Profit": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["netIncome"],
            "Cash Flow": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["operatingCashflow"]
        })
        return company_dfs
