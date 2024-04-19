import pandas as pd
from BackEnd.companydata import get_ticker_balance_df_adj, APICompanyData


class TestCompanyData:

    # tests the cash flow calculation operation
    def test_ticker_balance_adjusted(self):
        balance_sheet = pd.DataFrame({
            "Operating Cash Flow": [100],
            "Cash Flow From Financing": [-50],
            "Cash Flow From Investment": [25],
            "Total Revenue": [0],
            "Profit": [0],
        })
        balance_sheet = get_ticker_balance_df_adj(balance_df=balance_sheet)
        assert balance_sheet["Cash Flow"].iloc[0] == 75

    def test_company_data_grab(self):
        ticker = "google"
        assert valid_ticker_input(ticker=ticker) is None
        ticker = get_formatted_ticker(ticker=ticker)
        nvidia_data = APICompanyData(ticker=ticker)

        nvidia_data_dfs = nvidia_data.ticker_df_data

        # check values are not less than 0 in ticker prices in Open, High, Close, Volume
        ticker_prices = nvidia_data_dfs["ticker_prices_df"]
        for df_name in ticker_prices:
            assert ticker_prices[ticker_prices[df_name] < 0].empty

        # check if values are greater than 0 for market cap, 52 week high, 52 week low
        ticker_overview = nvidia_data_dfs["ticker_overview_df"]
        assert ticker_overview["Market Cap"].iloc[0] > 0
        assert ticker_overview["52 Week High"].iloc[0] > 0
        assert ticker_overview["52 Week Low"].iloc[0] > 0

    def test_company_data_grab_filtration(self):
        ticker = "LULU"
        lulu_data = APICompanyData(ticker=ticker).ticker_df_data

        # checks if values are not null or 'None'
        for df_name, df in lulu_data.items():
            for column in df:
                assert df[column].isna().sum() == 0
                assert df[df[column] == "None"].empty