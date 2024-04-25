import numpy as np
import pandas as pd

from BackEnd.companydata import CompanyData


def find_closest_dates_before(date, prices_df):
    return prices_df[prices_df.index < date].first_valid_index()


def find_closest_dates_after(date, prices_df):
    return prices_df[prices_df.index > date].last_valid_index()


class DataDifferentials:
    """
    1) gather data of balance sheet + eps report
    2) gather prices before and after earnings report dates
    3) get price differentials of each day
    4) linear regression of correlation between eps data or balance sheet data to price differentials
    """

    def __init__(self, company: type(CompanyData)):
        self.report_prices_df = self.get_price_differentials_earnings(company_prices_df=company.company_prices)
        self.report_eps_df = self.get_eps_differentials(company_prices_df=self.report_prices_df, company_eps_df=company.company_eps)
        self.report_balance_sheet_df = self.get_balance_sheet_differentials(company_prices_df=self.report_prices_df, company_balance_sheet_df=company.company_balance_sheet)
        self.report_companydata_df = self.get_all_data_differentials(company_prices_df=self.report_prices_df, company_eps_df=company.company_eps, company_balance_sheet_df=company.company_balance_sheet)

    def get_price_differentials_earnings(self, company_prices_df: pd.DataFrame):
        years = list(set(company_prices_df.index.year))
        start_year = years[1]
        recent_year = years[-2]

        quarter_dates = ["03-31", "06-30", "09-30", "12-31"]

        report_dates = sorted(set(pd.Timestamp(f"{year}-{q}") for year in range(start_year, recent_year + 1) for q in quarter_dates))

        before_dates = [find_closest_dates_before(date, company_prices_df) for date in report_dates]
        after_dates = [find_closest_dates_after(date, company_prices_df) for date in report_dates]

        combined_report_dates = report_dates + before_dates + after_dates

        prices_report_dates_df = company_prices_df[(company_prices_df.index.isin(combined_report_dates))]
        prices_report_dates_df["Report"] = np.select(condlist=[
            prices_report_dates_df.index.isin(before_dates),
            prices_report_dates_df.index.isin(after_dates),
            prices_report_dates_df.index.isin(report_dates)],
            choicelist=["before", "after", "report"],
            default=np.nan
        )

        prices_report_dates_df.reset_index(inplace=True, names="Date")
        before_report = prices_report_dates_df[ prices_report_dates_df["Report"] == "before"]["Close"].reset_index(drop=True)
        after_report = prices_report_dates_df[ prices_report_dates_df["Report"] == "after"]["Close"].reset_index(drop=True)
        report_differentials = ((after_report - before_report) / before_report) * 100

        report_price_differentials = pd.DataFrame({
            "Before Report Price": before_report,
            "After Report Price": after_report,
            "Diff Percentage Reports": report_differentials
        })

        report_price_differentials.index = report_dates[::-1]
        return report_price_differentials

    def get_eps_differentials(self, company_prices_df: pd.DataFrame, company_eps_df: pd.DataFrame):
        company_eps_df = company_eps_df[company_eps_df.index.isin(company_prices_df.index)]
        company_eps_reports = pd.merge(company_prices_df, company_eps_df, right_index=True, left_index=True)
        return company_eps_reports[["Diff Percentage Reports", "surprisePercentage"]]

    def get_balance_sheet_differentials(self, company_prices_df, company_balance_sheet_df: pd.DataFrame):
        company_prices_df = company_prices_df[company_prices_df.index.isin(company_balance_sheet_df.index)]
        company_balance_sheet_report = pd.merge(company_prices_df, company_balance_sheet_df, left_index=True, right_index=True)
        return company_balance_sheet_report

    def get_all_data_differentials(self, company_prices_df: pd.DataFrame, company_eps_df: pd.DataFrame, company_balance_sheet_df: pd.DataFrame):
        company_prices_df = company_prices_df[(company_prices_df.index.isin(company_eps_df.index)) & (company_prices_df.index.isin(company_balance_sheet_df.index))]
        company_report_data = pd.concat([company_prices_df, company_eps_df, company_balance_sheet_df], axis=1).dropna()
        return company_report_data
