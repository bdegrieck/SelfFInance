from BackEnd.Data.api import get_raw_api_data, get_company_endpoints, get_company_dfs


class CompanyData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        endpoints = get_company_endpoints(ticker=self.ticker)
        raw_data = get_raw_api_data(endpoints=endpoints)
        company_df_data = get_company_dfs(company_raw_data=raw_data)
        self.company_prices = company_df_data["ticker_prices_df"]
        self.company_overview = company_df_data["ticker_overview_df"]
        self.company_eps = company_df_data["ticker_eps_df"]
        self.company_balance_sheet = company_df_data["ticker_balance_df"]
