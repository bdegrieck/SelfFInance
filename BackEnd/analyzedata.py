import datetime

import pandas as pd

from BackEnd.companydata import CompanyData


class AnalyzeData:
    """
    1) gather data of balance sheet + eps report
    2) gather prices before and after earnings report dates
    3) get price differentials of each day
    4) linear regression of correlation between eps data or balance sheet data to price differentials
    """

    def __init__(self, company: type(CompanyData)):
        self.company_prices = company.company_prices
        self.company_eps = company.company_eps
        self.company_balance_sheet = company.company_balance_sheet
        self.company_overview = company.company_overview
        self.quarter_dates = self.get_prices_near_earnings(company_df_prices=self.company_prices)

    def get_prices_near_earnings(self, company_df_prices: pd.DataFrame):
        quarter_months = [3, 6, 9, 12]
        prices_dates = company_df_prices[(company_df_prices.index.month in quarter_months) & (company_df_prices.index.day == 31)]
        return prices_dates


