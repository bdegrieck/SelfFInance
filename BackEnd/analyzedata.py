import datetime

import pandas as pd

from BackEnd.companydata import CompanyData


def find_closest_dates_before(date, prices_df):
    return prices_df[prices_df.index < date].first_valid_index()


def find_closest_dates_after(date, prices_df):
    return prices_df[prices_df.index > date].last_valid_index()


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
        self.quarter_dates = self.get_prices_near_earnings(company_df_prices=self.company_prices, company_reports=self.company_balance_sheet)

    def get_prices_near_earnings(self, company_df_prices: pd.DataFrame, company_reports: pd.DataFrame):
        years = list(set(company_df_prices.index.year))
        before_dates = []
        after_dates = []

        start_year = years[1]
        recent_year = years[-2]

        report_dates = sorted((set(pd.date_range(start=f"{start_year}-03-31", end=f"{recent_year}-03-31", freq="A-MAR")) |
                        set(pd.date_range(start=f"{start_year}-06-30", end=f"{recent_year}-06-30", freq="A-JUN")) |
                        set(pd.date_range(start=f"{start_year}-09-30", end=f"{recent_year}-09-30", freq="A-SEP")) |
                        set(pd.date_range(start=f"{start_year}-12-31", end=f"{recent_year}-12-31", freq="A-DEC"))))

        for date in report_dates:
            before_dates.append(find_closest_dates_before(date, company_df_prices))
            after_dates.append(find_closest_dates_after(date, company_df_prices))

        prices_report_dates = company_df_prices[(company_df_prices.index.isin(before_dates)) | (company_df_prices.index.isin(report_dates)) | (company_df_prices.index.isin(after_dates))]
        return recent_year


