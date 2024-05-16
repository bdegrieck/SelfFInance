import pandas as pd

from BackEnd.Data.companydata import CompanyData


class TickerComparison:
    def __init__(self, main_ticker_data: type(CompanyData), second_ticker_data: type(CompanyData)):
        self.main_ticker_data = main_ticker_data
        self.second_ticker_data = second_ticker_data
        self.data_comparison = self.compare_financials()

    # compares company financials: ticker prices, market cap, eps, revenue, and profit
    def compare_financials(self) -> pd.DataFrame:
        main_market_cap = self.main_ticker_data.company_overview.market_cap
        second_market_cap = self.second_ticker_data.company_overview.market_cap
        market_cap_diff = abs(main_market_cap - second_market_cap)

        main_ticker_price = self.main_ticker_data.company_dfs.stock_data_df["close"].iloc[0]
        second_ticker_price = self.second_ticker_data.company_dfs.stock_data_df["close"].iloc[0]
        ticker_price_dff = abs(main_ticker_price - second_ticker_price)

        main_reported_EPS = self.main_ticker_data.company_dfs.eps_df["reportedEPS"].iloc[0]
        second_reported_EPS = self.second_ticker_data.company_dfs.eps_df["reportedEPS"].iloc[0]
        reported_EPS_diff = abs(main_reported_EPS - second_reported_EPS)

        main_revenue = self.main_ticker_data.company_dfs.balance_sheet_df["revenue"].iloc[0]
        second_revenue = self.second_ticker_data.company_dfs.balance_sheet_df["revenue"].iloc[0]
        revenue_diff = abs(main_revenue - second_revenue)

        main_profit = self.main_ticker_data.company_dfs.balance_sheet_df["profit"].iloc[0]
        second_profit = self.second_ticker_data.company_dfs.balance_sheet_df["profit"].iloc[0]
        profit_diff = abs(main_profit - second_profit)

        main_price_per_earnings = main_ticker_price/main_reported_EPS
        second_price_per_earnings = second_ticker_price/second_reported_EPS
        price_per_earnings_diff = abs(main_price_per_earnings - second_price_per_earnings)

        company_comparison_df = pd.DataFrame({
            "companies": [self.main_ticker_data.ticker, self.second_ticker_data.ticker, "Difference"],
            "prices": [main_ticker_price, second_ticker_price, ticker_price_dff],
            "marketCap": [main_market_cap, second_market_cap, market_cap_diff],
            "reportedEPS": [main_reported_EPS, second_reported_EPS, reported_EPS_diff],
            "revenue": [main_revenue, second_revenue, revenue_diff],
            "profit": [main_profit, second_profit, profit_diff],
            "pricePerEarnings": [main_price_per_earnings, second_price_per_earnings, price_per_earnings_diff]
        }).set_index("companies")

        return company_comparison_df

