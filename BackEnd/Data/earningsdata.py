import numpy as np
import pandas as pd

from BackEnd.Data.calender import EarningsCalender
from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.microdata import MicroData
from BackEnd.Data.techindicators import TechnicalIndicators
from BackEnd.routines import get_shifted_differences, get_series_difference_percentage, find_closest_dates_before, \
    find_closest_dates_after


class EarningsData:

    def __init__(self, stock_data: CompanyData, technical_analysis_data: TechnicalIndicators, calender: EarningsCalender, micro_data: MicroData):
        report_dates_dict = {index: date for index, date in zip(stock_data.report_dates.index, stock_data.report_dates)}
        self.quarter_dates = set(stock_data.company_dfs.balance_sheet_df.index)
        self.report_eps_differences_df = self.get_eps_differences(company_eps_df=stock_data.company_dfs.eps_df)
        self.report_balance_sheet_differences_df = self.get_balance_sheet_differences(company_balance_sheet_df=stock_data.company_dfs.balance_sheet_df)
        self.report_prices_differences_df = self.get_price_differences(
            company_prices_df=stock_data.company_dfs.stock_data_df,
            report_dates=report_dates_dict
        )

    def get_price_differences(self, company_prices_df: pd.DataFrame, report_dates: dict) -> pd.DataFrame:

        # finds closest dates in prices_df closest to the report date and removes 0 from report dates
        combined_report_dates = set()
        before_dates = []
        after_dates = []
        filtered_report_dates = []
        filtered_quarter_dates = []

        for quarter_date, report_date in report_dates.items():
            before_date = find_closest_dates_before(report_date, company_prices_df)
            after_date = find_closest_dates_after(quarter_date, company_prices_df)

            # Use set union to combine dates without duplicates
            if before_date and after_date is not None:
                combined_report_dates.update({report_date, before_date, after_date})
                before_dates.append(before_date)
                after_dates.append(after_date)
                filtered_report_dates.append(report_date)
                filtered_quarter_dates.append(quarter_date)

        # gets all rows where the date is before and after earning reports
        prices_report_dates_df = company_prices_df[company_prices_df.index.isin(combined_report_dates)]
        prices_report_dates_df["report"] = np.select(condlist=[
            prices_report_dates_df.index.isin(before_dates),
            prices_report_dates_df.index.isin(after_dates),
            prices_report_dates_df.index.isin(filtered_report_dates)],
            choicelist=["before", "after", "report"],
            default=np.nan
        )

        # calculates price change before and after report closing price
        before_report_prices = prices_report_dates_df[prices_report_dates_df["report"] == "before"]["close"].reset_index(drop=True)
        after_report_prices = prices_report_dates_df[prices_report_dates_df["report"] == "after"]["close"].reset_index(drop=True)
        report_differences = get_series_difference_percentage(series1=before_report_prices, series2=after_report_prices)

        report_price_differences_df = pd.DataFrame({
            "reportedDate": sorted(filtered_report_dates, reverse=True),
            "beforeReportPrice": before_report_prices,
            "afterReportPrice": after_report_prices,
            "priceDiffPercentage": report_differences
        })

        report_price_differences_df = get_shifted_differences(
            df=report_price_differences_df,
            columns_to_shift=["beforeReportPrice", "afterReportPrice", "priceDiffPercentage"],
            shift_motion=-1
        )

        # handles index
        report_price_differences_df.index = filtered_quarter_dates

        # drops na values
        report_price_differences_df = report_price_differences_df.dropna()

        return report_price_differences_df

    def get_eps_differences(self, company_eps_df: pd.DataFrame) -> pd.DataFrame:

        # calculates eps data differences
        company_eps_df["estimatedEPSDiffPercentage"] = (
            ((company_eps_df["estimatedEPS"] - company_eps_df["estimatedEPS"].shift(-1)) / company_eps_df["estimatedEPS"].shift(-1))
        )
        company_eps_df["reportedEPSDiffPercentage"] = (
                ((company_eps_df["reportedEPS"] - company_eps_df["reportedEPS"].shift(-1)) / company_eps_df["reportedEPS"].shift(-1))
        )
        company_eps_df["surprisePercentageDiffPercentage"] = (
                ((company_eps_df["surprisePercentage"] - company_eps_df["surprisePercentage"].shift(-1)) / company_eps_df["surprisePercentage"].shift(-1))
        )

        return company_eps_df

    def get_balance_sheet_differences(self, company_balance_sheet_df: pd.DataFrame) -> pd.DataFrame:
        company_balance_sheet_diff = company_balance_sheet_df[["cashFlow", "revenue", "profit"]]

        # calculates differences between quarterly reports
        company_balance_sheet_diff["revenueDiff"] = (
            (company_balance_sheet_df["revenue"] - company_balance_sheet_df["revenue"].shift(-1))
        )
        company_balance_sheet_diff["profitDiff"] = (
            (company_balance_sheet_df["profit"] - company_balance_sheet_df["profit"].shift(-1))
        )
        company_balance_sheet_diff["cashFlowDiff"] = (
            (company_balance_sheet_df["cashFlow"] - company_balance_sheet_df["cashFlow"].shift(-1))
        )

        return company_balance_sheet_diff
