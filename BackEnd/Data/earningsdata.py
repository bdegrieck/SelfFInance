import numpy as np
import pandas as pd
from pandas import Timestamp

from BackEnd.Data.techindicators import TechnicalIndicators


def find_closest_dates_before(date, data_df):
    return data_df[data_df.index < date].first_valid_index()


def find_closest_dates_after(date, data_df):
    return data_df[data_df.index > date].last_valid_index()


class EarningsData:

    def __init__(self, stock_data):
        report_dates = set(stock_data.company_balance_sheet["reportedDate"])
        self.quarter_dates = stock_data.company_eps.index
        self.report_eps_differences_df = self.get_eps_differences(company_eps_df=stock_data.company_eps, quarter_dates=self.quarter_dates)
        self.report_balance_sheet_differences_df = self.get_balance_sheet_differences(company_balance_sheet_df=stock_data.company_balance_sheet)
        self.report_prices_differences_df = self.get_price_differences(company_prices_df=stock_data.company_prices, report_dates=report_dates)
        technical_analysis_raw_data = TechnicalIndicators(ticker=stock_data.ticker).technical_indicator_data
        self.technical_analysis_data_df = self.get_technical_analysis_earnings_data(tech_analysis_raw_data=technical_analysis_raw_data, report_dates=report_dates)

    def get_price_differences(self, company_prices_df: pd.DataFrame, report_dates: set) -> pd.DataFrame:
        # finds closest dates in prices_df closest to the report date and removes 0 from report dates
        combined_report_dates = set()
        before_dates_dict = {}
        after_dates_dict = {}
        report_dates = sorted({date for date in report_dates if date != 0 and date > self.report_eps_differences_df.index[-1]}, reverse=True)

        for date in report_dates:
            before_date = find_closest_dates_before(date, company_prices_df)
            after_date = find_closest_dates_after(date, company_prices_df)

            # Check if before_date is not equal to 0 before adding to before_dates_dict
            if before_date is not None:
                before_dates_dict[date] = before_date

            if after_date is not None:
                after_dates_dict[date] = after_date

            # Use set union to combine dates without duplicates
            combined_report_dates.update({date, before_date, after_date})

        # gets all rows where the date is before and after earning reports
        prices_report_dates_df = company_prices_df[(company_prices_df.index.isin(combined_report_dates))]
        prices_report_dates_df["report"] = np.select(condlist=[
            prices_report_dates_df.index.isin(before_dates_dict.values()),
            prices_report_dates_df.index.isin(after_dates_dict.values()),
            prices_report_dates_df.index.isin(report_dates)],
            choicelist=["before", "after", "report"],
            default=np.nan
        )

        # calculates price change before and after report closing price
        before_report_prices = prices_report_dates_df[prices_report_dates_df["report"] == "before"]["close"].reset_index(drop=True)
        after_report_prices = prices_report_dates_df[prices_report_dates_df["report"] == "after"]["close"].reset_index(drop=True)

        # if earnings was day of the the program run then before and after would be uneven since after hasn't happened yet
        if len(before_dates_dict) == len(after_dates_dict) + 1:
            before_report_prices = before_report_prices.drop([0]).reset_index(drop=True)
            report_dates.pop(0)

        # if there is a report and closing price the next day hasn't been out yet
        if len(report_dates) == len(before_dates_dict) + 1:
            report_dates.pop(0)

        report_differences = ((after_report_prices - before_report_prices) / before_report_prices) * 100
        report_price_differences = pd.DataFrame({
            "reportedDate": report_dates,
            "beforeReportPrice": before_report_prices,
            "afterReportPrice": after_report_prices,
            "priceDiffPercentage": report_differences
        })

        report_price_differences["beforeReportPriceDiffPercentage"] = (
            (report_price_differences["beforeReportPrice"] - report_price_differences["beforeReportPrice"].shift(-1)) / report_price_differences["beforeReportPrice"].shift(-1))
        report_price_differences["afterReportPriceDiffPercentage"] = (
            (report_price_differences["afterReportPrice"] - report_price_differences["afterReportPrice"].shift(-1)) / report_price_differences["afterReportPrice"].shift(-1))
        report_price_differences["priceDiffPercentageDiff"] = (
            (report_price_differences["priceDiffPercentage"] - report_price_differences["priceDiffPercentage"].shift(-1)) / report_price_differences["priceDiffPercentage"].shift(-1))

        # handles index
        quarter_dates = ["03-31", "06-30", "09-30", "12-31"]
        first_quarter_year = self.report_eps_differences_df.index[-1].year
        most_recent_quarter_year = self.report_eps_differences_df.index[0].year
        most_recent_quarter = self.report_eps_differences_df.index[0]
        list_of_quarter_dates = [Timestamp(f"{year}-{quarter_date}") for year in range(first_quarter_year, most_recent_quarter_year + 1) for quarter_date in quarter_dates]

        list_index = [date for date in list_of_quarter_dates if date <= most_recent_quarter]


        index_length = len(report_price_differences)
        report_price_differences.index = list_index[-index_length:][::-1]

        return report_price_differences

    def get_eps_differences(self, quarter_dates: set, company_eps_df: pd.DataFrame) -> pd.DataFrame:
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
        company_balance_sheet_diff = pd.DataFrame({
            "totalRevenue": company_balance_sheet_df["totalRevenue"],
            "profit": company_balance_sheet_df["profit"],
            "cashFlow": company_balance_sheet_df["cashFlow"]
        })

        # calculates differences between quarterly reports
        company_balance_sheet_diff["totalRevenueDiff"] = (
            (company_balance_sheet_df["totalRevenue"] - company_balance_sheet_df["totalRevenue"].shift(-1))
        )
        company_balance_sheet_diff["profitDiff"] = (
            (company_balance_sheet_df["profit"] - company_balance_sheet_df["profit"].shift(-1))
        )
        company_balance_sheet_diff["cashFlowDiff"] = (
            (company_balance_sheet_df["cashFlow"] - company_balance_sheet_df["cashFlow"].shift(-1))
        )

        return company_balance_sheet_diff

    def get_technical_analysis_earnings_data(self, tech_analysis_raw_data: pd.DataFrame, report_dates: set):
        technical_analysis_earnings_dict = {}
        for tech_analysis_name, tech_analysis_value in tech_analysis_raw_data.items():
            tech_analysis_dates = set()
            for date in report_dates:
                tech_analysis_dates.add(find_closest_dates_before(
                    data_df=tech_analysis_value["Technical Analysis Data"],
                    date=date,
                ))
            technical_analysis_earnings_dict[tech_analysis_name] = tech_analysis_value["Technical Analysis Data"][tech_analysis_value["Technical Analysis Data"].index.isin(tech_analysis_dates)]
        return technical_analysis_earnings_dict
