import numpy as np
import pandas as pd


def find_closest_dates_before(date, prices_df):
    return prices_df[prices_df.index < date].first_valid_index()


def find_closest_dates_after(date, prices_df):
    return prices_df[prices_df.index > date].last_valid_index()


class ReportDifferences:

    def __init__(self, company_balance_sheet: pd.DataFrame, company_prices: pd.DataFrame, company_eps: pd.DataFrame):
        self.report_dates = set(company_balance_sheet["reportedDate"])
        self.report_prices_differences_df = self.get_price_differences(company_prices_df=company_prices, report_dates=self.report_dates)
        self.report_eps_differences_df = self.get_eps_differences(company_eps_df=company_eps, report_dates=company_eps.index)
        self.report_balance_sheet_differences_df = self.get_balance_sheet_differences(company_balance_sheet_df=company_balance_sheet)
        self.report_differences_df = self.get_all_data_differences(company_prices_df=self.report_prices_differences_df, company_eps_df=self.report_eps_differences_df, company_balance_sheet_df=self.report_balance_sheet_differences_df)

    def get_price_differences(self, company_prices_df: pd.DataFrame, report_dates: set) -> pd.DataFrame:
        # finds closest dates in prices_df closest to the report date
        before_dates = set(find_closest_dates_before(date, company_prices_df) for date in report_dates)
        after_dates = set(find_closest_dates_after(date, company_prices_df) for date in report_dates)
        combined_report_dates = report_dates | before_dates | after_dates

        # gets all rows where the date is before and after earning reports
        prices_report_dates_df = company_prices_df[(company_prices_df.index.isin(combined_report_dates))]
        prices_report_dates_df["report"] = np.select(condlist=[
            prices_report_dates_df.index.isin(before_dates),
            prices_report_dates_df.index.isin(after_dates),
            prices_report_dates_df.index.isin(report_dates)],
            choicelist=["before", "after", "report"],
            default=np.nan
        )

        # calculates price change before and after report closing price
        before_report = prices_report_dates_df[prices_report_dates_df["report"] == "before"]["close"].reset_index(drop=True)
        after_report = prices_report_dates_df[prices_report_dates_df["report"] == "after"]["close"].reset_index(drop=True)
        report_differentials = ((after_report - before_report) / before_report) * 100
        report_price_differentials = pd.DataFrame({
            "reportedDate": sorted(report_dates, reverse=True),
            "beforeReportPrice": before_report,
            "afterReportPrice": after_report,
            "priceDiffPercentage": report_differentials
        })

        # calculates price differential percentage between quarters of before, after and price percentage differential
        report_price_differentials["beforeReportPriceDiffPercentage"] = (
            (report_price_differentials["beforeReportPrice"] - report_price_differentials["beforeReportPrice"].shift(-1)) / report_price_differentials["beforeReportPrice"].shift(-1)) * 100
        report_price_differentials["afterReportPriceDiffPercentage"] = (
            (report_price_differentials["afterReportPrice"] - report_price_differentials["afterReportPrice"].shift(-1)) / report_price_differentials["afterReportPrice"].shift(-1)) * 100
        report_price_differentials["priceDiffPercentageDiff"] = (
            (report_price_differentials["priceDiffPercentage"] - report_price_differentials["priceDiffPercentage"].shift(-1)) / report_price_differentials["priceDiffPercentage"].shift(-1)) * 100

        return report_price_differentials

    def get_eps_differences(self, report_dates: set, company_eps_df: pd.DataFrame) -> pd.DataFrame:
        # filters out eps data that is not in price df
        company_eps_df = company_eps_df[company_eps_df.index.isin(report_dates)]

        # calculates eps data differences
        company_eps_df["estimatedEPSDiffPercentage"] = (
            ((company_eps_df["estimatedEPS"] - company_eps_df["estimatedEPS"].shift(-1)) / company_eps_df["estimatedEPS"].shift(-1)) * 100
        )
        company_eps_df["reportedEPSDiffPercentage"] = (
                ((company_eps_df["reportedEPS"] - company_eps_df["reportedEPS"].shift(-1)) / company_eps_df["reportedEPS"].shift(-1)) * 100
        )
        company_eps_df["surprisePercentageDiffPercentage"] = (
                ((company_eps_df["surprisePercentage"] - company_eps_df["surprisePercentage"].shift(-1)) / company_eps_df["surprisePercentage"].shift(-1)) * 100
        )

        return company_eps_df

    def get_balance_sheet_differences(self, company_balance_sheet_df: pd.DataFrame) -> pd.DataFrame:
        # calculates differences between quarterly reports
        company_balance_sheet_df["totalRevenueDiff"] = (
            ((company_balance_sheet_df["totalRevenue"] - company_balance_sheet_df["totalRevenue"].shift(-1)) * 100)
        )
        company_balance_sheet_df["profitDiff"] = (
            ((company_balance_sheet_df["profit"] - company_balance_sheet_df["profit"].shift(-1)) * 100)
        )
        company_balance_sheet_df["cashFlowDiff"] = (
            ((company_balance_sheet_df["cashFlow"] - company_balance_sheet_df["cashFlow"].shift(-1)) * 100)
        )
        return company_balance_sheet_df

    def get_all_data_differences(self, company_prices_df: pd.DataFrame, company_eps_df: pd.DataFrame, company_balance_sheet_df: pd.DataFrame) -> pd.DataFrame:
        company_prices_df.index = list(company_balance_sheet_df.index)
        company_prices_df = company_prices_df[(company_prices_df.index.isin(company_eps_df.index)) & (company_prices_df.index.isin(company_balance_sheet_df.index))]
        data_differences_merged = pd.merge(company_prices_df, company_eps_df, how="outer", on="reportedDate").merge(company_balance_sheet_df, on="reportedDate", how="outer").set_index(company_eps_df.index[::-1])
        return data_differences_merged[(data_differences_merged != 0).all(axis=1)].dropna()[::-1]
