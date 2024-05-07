from BackEnd.Data.api import API
from BackEnd.Data.earningsdata import EarningsData


class CompanyData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        raw_data = API(ticker=ticker)
        self.company_prices = raw_data.ticker_df_data["ticker_prices_df"]
        self.company_overview = raw_data.ticker_df_data["ticker_overview_df"]
        self.company_eps = raw_data.ticker_df_data["ticker_eps_df"]
        self.company_balance_sheet = raw_data.ticker_df_data["ticker_balance_df"]
