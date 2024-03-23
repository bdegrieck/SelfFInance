import pandas as pd

from BackEnd.companyData import CompanyData

class Compare:
    def __init__(self, main_ticker_data: type(CompanyData), second_ticker_data: type(CompanyData)):
        self.main_ticker_data = main_ticker_data
        self.second_ticker_data = second_ticker_data
        self.data_comparison = self.compare_financials()

    def compare_financials(self) -> pd.DataFrame:
        main_market_cap = self.main_ticker_data.ticker_df_data["ticker_overview_df"]["Market Cap"].iloc[0]
        second_market_cap = self.second_ticker_data.ticker_df_data["ticker_overview_df"]["Market Cap"].iloc[0]
        market_cap_diff = abs(main_market_cap - second_market_cap)

        main_ticker_price = self.main_ticker_data.ticker_df_data["ticker_prices_df"]["Close"].iloc[0]
        second_ticker_price = self.second_ticker_data.ticker_df_data["ticker_prices_df"]["Close"].iloc[0]
        ticker_price_dff = abs(main_ticker_price - second_ticker_price)

        main_reported_EPS = self.main_ticker_data.ticker_df_data["ticker_eps_df"]["reportedEPS"].iloc[0]
        second_reported_EPS = self.second_ticker_data.ticker_df_data["ticker_eps_df"]["reportedEPS"].iloc[0]
        reported_EPS_diff = abs(main_reported_EPS - second_reported_EPS)

        main_revenue = self.main_ticker_data.ticker_df_data["ticker_balance_df"]["Total Revenue"].iloc[0]
        second_revenue = self.second_ticker_data.ticker_df_data["ticker_balance_df"]["Total Revenue"].iloc[0]
        revenue_diff = abs(main_revenue - second_revenue)

        main_profit = self.main_ticker_data.ticker_df_data["ticker_balance_df"]["Profit"].iloc[0]
        second_profit = self.second_ticker_data.ticker_df_data["ticker_balance_df"]["Profit"].iloc[0]
        profit_diff = abs(main_profit - second_profit)

        main_price_per_earnings = main_ticker_price/main_reported_EPS
        second_price_per_earnings = second_ticker_price/second_reported_EPS
        price_per_earnings_diff = abs(main_price_per_earnings - second_price_per_earnings)

        return pd.DataFrame({
            "Companies": [self.main_ticker_data.ticker, self.second_ticker_data.ticker, "Difference"],
            "Prices": [main_ticker_price, second_ticker_price, ticker_price_dff],
            "Market Cap": [main_market_cap, second_market_cap, market_cap_diff],
            "Reported EPS": [main_reported_EPS, second_reported_EPS, reported_EPS_diff],
            "Revenue": [main_revenue, second_revenue, revenue_diff],
            "Profit": [main_profit, second_profit, profit_diff],
            "Price Per Earnings": [main_price_per_earnings, second_price_per_earnings, price_per_earnings_diff]
        }).set_index("Companies")

