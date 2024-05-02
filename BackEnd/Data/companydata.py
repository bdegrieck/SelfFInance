from BackEnd.Data.api import API
from BackEnd.Data.reportdifferences import ReportDifferences


class CompanyData:

    def __init__(self, ticker: str):
        raw_data = API(ticker=ticker)
        self.company_prices = raw_data.ticker_df_data["ticker_prices_df"]
        self.company_overview = raw_data.ticker_df_data["ticker_overview_df"]
        self.company_eps = raw_data.ticker_df_data["ticker_eps_df"]
        self.company_balance_sheet = raw_data.ticker_df_data["ticker_balance_df"]
        self.company_report_differences = ReportDifferences(company_balance_sheet=self.company_balance_sheet, company_eps=self.company_eps, company_prices=self.company_prices)



