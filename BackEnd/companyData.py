from BackEnd.data import get_raw_api_data, get_html
import pandas as pd



class CompanyData:

    def __init__(self, ticker: str, api_key: str):
        self.ticker = ticker
        self.api_key = api_key
        self.ticker_endpoints = self.get_endpoint_company()
        self.ticker_raw_data = get_raw_api_data(endpoints=self.ticker_endpoints)
        self.ticker_df_data = self.get_company_df_data()
        self.ticker_html_data = get_html(df_data=self.ticker_df_data)
        print("hi")

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
        company_dfs["ticker_prices_df"] = self.get_ticker_prices_df_adj(prices_df=company_dfs["ticker_prices_df"].astype(float))

        company_dfs["ticker_overview_df"] = pd.DataFrame({
            "Ticker Symbol": [self.ticker_raw_data["overview"]["Symbol"]],
            "Company Description": [self.ticker_raw_data["overview"]["Description"]],
            "Market Cap": [float(self.ticker_raw_data["overview"]["MarketCapitalization"])],
            "52 Week High": [float(self.ticker_raw_data["overview"]["52WeekHigh"])],
            "52 Week Low": [float(self.ticker_raw_data["overview"]["52WeekLow"])]
        })

        company_dfs["ticker_eps_df"] = pd.DataFrame(self.ticker_raw_data["earnings"]["quarterlyEarnings"])
        company_dfs["ticker_eps_df"] = self.get_ticker_eps_df_adj(eps_df=company_dfs["ticker_eps_df"])

        company_dfs["ticker_balance_df"] = pd.DataFrame({
            "Date": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["fiscalDateEnding"],
            "Total Revenue": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["totalRevenue"].astype(float),
            "Profit": pd.DataFrame(self.ticker_raw_data["income_statement"]["quarterlyReports"])["netIncome"].astype(float),
            "Operating Cash Flow": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["operatingCashflow"].astype(float),
            "Cash Flow From Financing": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromFinancing"].astype(float),
            "Cash Flow From Investment": pd.DataFrame(self.ticker_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromInvestment"].astype(float)
        })
        company_dfs["ticker_balance_df"] = self.get_ticker_balance_df_adj(company_dfs["ticker_balance_df"])

        return company_dfs

    def get_ticker_prices_df_adj(self, prices_df: pd.DataFrame) -> pd.DataFrame:
        prices_df.columns = ["Open", "High", "Low", "Adjusted Close", "Close", "Volume", "Dividends", "Splits"]
        return prices_df[["Open", "High", "Low", "Adjusted Close", "Volume"]]

    def get_ticker_eps_df_adj(self, eps_df: pd.DataFrame) -> pd.DataFrame:
        eps_df.replace('None', 0, inplace=True)
        eps_df = eps_df.set_index("fiscalDateEnding")[["estimatedEPS", "surprise", "surprisePercentage"]].astype(float)
        return eps_df

    def get_ticker_balance_df_adj(self, balance_df: pd.DataFrame) -> pd.DataFrame:
        balance_df = balance_df.set_index("Date").fillna(0)
        balance_df["Cash Flow"] = balance_df[["Operating Cash Flow", "Cash Flow From Financing", "Cash Flow From Investment"]].sum(axis=1)
        return balance_df[["Total Revenue", "Profit", "Cash Flow"]]
