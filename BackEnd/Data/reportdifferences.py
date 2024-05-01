import numpy as np
import pandas as pd

from BackEnd.Data.companydata import CompanyData


def find_closest_dates_before(date, prices_df):
    return prices_df[prices_df.index < date].first_valid_index()


def find_closest_dates_after(date, prices_df):
    return prices_df[prices_df.index > date].last_valid_index()


class DataDifferences:

    def __init__(self, company: type(CompanyData)):
        self.report_dates = list(company.company_balance_sheet.index)
        self.report_prices_differences_df = self.get_price_differences(company_prices_df=company.company_prices, report_dates=self.report_dates)
        self.report_eps_differences_df = self.get_eps_differences(report_dates=self.report_dates, company_eps_df=company.company_eps)
        self.report_balance_sheet_differences_df = self.get_balance_sheet_differences(company_balance_sheet_df=company.company_balance_sheet)
        self.report_differences_df = self.get_all_data_differences(company_prices_df=self.report_prices_differences_df, company_eps_df=self.report_eps_differences_df, company_balance_sheet_df=self.report_balance_sheet_differences_df)

    def get_price_differences(self, company_prices_df: pd.DataFrame, report_dates: list) -> pd.DataFrame:
        # finds closest dates in prices_df closest to the report date
        before_dates = [find_closest_dates_before(date, company_prices_df) for date in report_dates]
        after_dates = [find_closest_dates_after(date, company_prices_df) for date in report_dates]
        combined_report_dates = report_dates + before_dates + after_dates

        # gets all rows where the date is before and after earning reports
        prices_report_dates_df = company_prices_df[(company_prices_df.index.isin(combined_report_dates))]
        prices_report_dates_df["Report"] = np.select(condlist=[
            prices_report_dates_df.index.isin(before_dates),
            prices_report_dates_df.index.isin(after_dates),
            prices_report_dates_df.index.isin(report_dates)],
            choicelist=["before", "after", "report"],
            default=np.nan
        )

        # calculates price change before and after report closing price
        prices_report_dates_df.reset_index(inplace=True, names="Date")
        before_report = prices_report_dates_df[ prices_report_dates_df["Report"] == "before"]["Close"].reset_index(drop=True)
        after_report = prices_report_dates_df[ prices_report_dates_df["Report"] == "after"]["Close"].reset_index(drop=True)
        report_differentials = ((after_report - before_report) / before_report) * 100
        report_price_differentials = pd.DataFrame({
            "Before Report Price": before_report,
            "After Report Price": after_report,
            "Price Diff Percentage": report_differentials
        })
        report_price_differentials.index = report_dates

        # calculates price differential percentage between quarters of before, after and price percentage differential
        report_price_differentials["Before Report Price Diff Percentage"] = (
            (report_price_differentials["Before Report Price"] - report_price_differentials["Before Report Price"].shift(-1)) / report_price_differentials["Before Report Price"].shift(-1)) * 100
        report_price_differentials["After Report Price Diff Percentage"] = (
            (report_price_differentials["Before Report Price"] - report_price_differentials["After Report Price"].shift(-1)) / report_price_differentials["After Report Price"].shift(-1)) * 100
        report_price_differentials["Price Diff Percentage Diff"] = (
            (report_price_differentials["Price Diff Percentage"] - report_price_differentials["Price Diff Percentage"].shift(-1)) / report_price_differentials["Price Diff Percentage"].shift(-1)) * 100

        return report_price_differentials

    def get_eps_differences(self, report_dates: list, company_eps_df: pd.DataFrame) -> pd.DataFrame:
        # filters out eps data that is not in price df
        company_eps_df = company_eps_df[company_eps_df.index.isin(report_dates)]

        # calculates eps data differences
        company_eps_df["estimatedEPS Diff Percentage"] = (
            ((company_eps_df["estimatedEPS"] - company_eps_df["estimatedEPS"].shift(-1)) / company_eps_df["estimatedEPS"].shift(-1)) * 100
        )
        company_eps_df["reportedEPS Diff Percentage"] = (
                ((company_eps_df["reportedEPS"] - company_eps_df["reportedEPS"].shift(-1)) / company_eps_df["reportedEPS"].shift(-1)) * 100
        )
        company_eps_df["surprisePercentage Diff Percentage"] = (
                ((company_eps_df["surprisePercentage"] - company_eps_df["surprisePercentage"].shift(-1)) / company_eps_df["surprisePercentage"].shift(-1)) * 100
        )

        return company_eps_df

    def get_balance_sheet_differences(self, company_balance_sheet_df: pd.DataFrame) -> pd.DataFrame:
        # calculates differences between quarterly reports
        company_balance_sheet_df["Total Revenue Diff"] = (
            ((company_balance_sheet_df["Total Revenue"] - company_balance_sheet_df["Total Revenue"].shift(-1)) * 100)
        )
        company_balance_sheet_df["Profit Diff"] = (
            ((company_balance_sheet_df["Profit"] - company_balance_sheet_df["Profit"].shift(-1)) * 100)
        )
        company_balance_sheet_df["Cash Flow Diff"] = (
            ((company_balance_sheet_df["Cash Flow"] - company_balance_sheet_df["Cash Flow"].shift(-1)) * 100)
        )
        return company_balance_sheet_df

    def get_all_data_differences(self, company_prices_df: pd.DataFrame, company_eps_df: pd.DataFrame, company_balance_sheet_df: pd.DataFrame) -> pd.DataFrame:
        company_prices_df = company_prices_df[(company_prices_df.index.isin(company_eps_df.index)) & (company_prices_df.index.isin(company_balance_sheet_df.index))]
        company_report_data = pd.concat([company_prices_df, company_eps_df, company_balance_sheet_df], axis=1).dropna()
        return company_report_data[(company_report_data != 0).all(axis=1)][::-1]
