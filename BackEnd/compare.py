import pandas as pd

from BackEnd.companyData import CompanyData

class Compare:
    def __init__(self, main_ticker_data: type(CompanyData), second_ticker_data: type(CompanyData)):
        self.main_ticker_data = main_ticker_data
        self.second_ticker_data = second_ticker_data
        self.data_comparison = self.compare_financials()

    def compare_financials(self) -> pd.DataFrame:
        main_market_cap = int(self.main_ticker_data.ticker_df_data["ticker_overview_df"]["Market Cap"].iloc[0])
        second_market_cap = int(self.second_ticker_data.ticker_df_data["ticker_overview_df"]["Market Cap"].iloc[0])
        market_cap_diff = abs(main_market_cap - second_market_cap)

        main_reported_EPS = float(self.main_ticker_data.ticker_df_data["ticker_eps_df"]["reportedEPS"].iloc[0])
        second_reported_EPS = float(self.second_ticker_data.ticker_df_data["ticker_eps_df"]["reportedEPS"].iloc[0])
        reported_EPS_diff = abs(main_reported_EPS - second_reported_EPS)

        main_profit = int(self.main_ticker_data.ticker_df_data["ticker_balance_df"]["Profit"].iloc[0])
        second_profit = int(self.second_ticker_data.ticker_df_data["ticker_balance_df"]["Profit"].iloc[0])
        profit_diff = abs(main_profit - second_profit)

        return pd.DataFrame({
            "Market Cap": [market_cap_diff],
            "Reported EPS": [reported_EPS_diff],
            "Profit": [profit_diff]
        })
