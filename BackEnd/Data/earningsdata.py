import numpy as np
import pandas as pd
from pandas import Timestamp

from BackEnd.Data.calender import EarningsCalender
from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.microdata import MicroData
from BackEnd.Data.techindicators import TechnicalIndicators
from BackEnd.routines import get_shifted_differences, get_series_difference_percentage


def find_closest_dates_before(date, data_df):
    return data_df[data_df.index < date].first_valid_index()


def find_closest_dates_after(date, data_df):
    return data_df[data_df.index > date].last_valid_index()


class EarningsData:

    def __init__(self, stock_data: CompanyData, technical_analysis_data: TechnicalIndicators, calender: EarningsCalender, micro_data: MicroData):
        report_dates = set(stock_data.company_dfs.eps_df.index)
        self.calender = calender
        self.quarter_dates = set(stock_data.company_dfs.balance_sheet_df.index)
        self.report_eps_differences_df = self.get_eps_differences(company_eps_df=stock_data.company_dfs.eps_df)
        self.report_balance_sheet_differences_df = self.get_balance_sheet_differences(company_balance_sheet_df=stock_data.company_dfs.balance_sheet_df)
        self.report_prices_differences_df = self.get_price_differences(company_prices_df=stock_data.company_dfs.stock_data_df, report_dates=report_dates)
        self.technical_analysis_data_dfs = self.get_technical_analysis_earnings_data(tech_analysis_raw_data=technical_analysis_data.technical_indicator_data, report_dates=report_dates)
        self.micro_data = self.get_micro_data(micro_data=micro_data, report_dates=report_dates)

    def get_price_differences(company_prices_df: pd.DataFrame, report_dates: dict) -> pd.DataFrame:

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
        before_report_prices = prices_report_dates_df[prices_report_dates_df["report"] == "before"][
            "close"].reset_index(drop=True)
        after_report_prices = prices_report_dates_df[prices_report_dates_df["report"] == "after"]["close"].reset_index(
            drop=True)
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

    def get_technical_analysis_earnings_data(self, tech_analysis_raw_data: pd.DataFrame, report_dates: set) -> dict:

        # filters out technical indicator df with report dates
        technical_analysis_earnings_dict = {}
        for tech_analysis_name, tech_analysis_value in tech_analysis_raw_data.items():
            tech_analysis_dates = set()
            for date in report_dates:
                tech_analysis_dates.add(find_closest_dates_before(
                    data_df=tech_analysis_value["Technical Analysis Data"],
                    date=date,
                ))
            technical_analysis_earnings_dict[tech_analysis_name] = tech_analysis_value["Technical Analysis Data"][tech_analysis_value["Technical Analysis Data"].index.isin(tech_analysis_dates)]

        # sets index of the technical indicator dfs with quarter dates instead of report dates
        for technical_indicator_name, technical_indicator_df in technical_analysis_earnings_dict.items():

            # handles index
            quarter_dates = ["03-31", "06-30", "09-30", "12-31"]
            first_quarter_year = self.report_eps_differences_df.index[-1].year
            most_recent_quarter_year = self.report_eps_differences_df.index[0].year
            most_recent_quarter = self.report_eps_differences_df.index[0]
            list_of_quarter_dates = [Timestamp(f"{year}-{quarter_date}") for year in range(first_quarter_year, most_recent_quarter_year + 1) for quarter_date in quarter_dates]

            list_index = [date for date in list_of_quarter_dates if date <= most_recent_quarter]

            index_length = len(technical_indicator_df)
            technical_indicator_df.index = list_index[-index_length:][::-1]

        return technical_analysis_earnings_dict

    def get_micro_data(self, micro_data, report_dates):

        # filters out technical indicator df with report dates
        micro_earnings_dict = {}
        for micro_name, micro_value in micro_data.items():
            micro_dates = set()
            for date in report_dates:
                micro_dates.add(find_closest_dates_before(
                    data_df=micro_value,
                    date=date,
                ))
            micro_earnings_dict[micro_name] = micro_value[micro_value.index.isin(micro_dates)]

        return micro_earnings_dict

    def get_upcoming_report_dates(self, earnings_calender):
        upcoming_company_calender = earnings_calender.company_earnings_calender["reportedDate"]
        return upcoming_company_calender
