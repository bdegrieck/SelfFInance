import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.reportdifferences import ReportDifferences


def format_data_for_model(stock_report):
    formatted_df = pd.merge(stock_report.report_balance_sheet_differences_df, stock_report.report_eps_differences_df, left_index=True, right_index=True)
    formatted_df = formatted_df.drop(columns=["reportedDate_x", "reportedDate_y"])
    return formatted_df


class OrdinaryLeastSquares:
    def __init__(self, company: type(CompanyData)):
        self.regr_model = linear_model.LinearRegression()
        company_report_differences = ReportDifferences(company_balance_sheet=company.company_balance_sheet, company_eps=company.company_eps, company_prices=company.company_prices)
        stock_report_formatted = format_data_for_model(stock_report=company_report_differences)
        self.least_ordinary_squares = self.get_ordinary_least_squares(linear_model=self.regr_model, stock_data=stock_report_formatted, stock_prices=company_report_differences.report_differences_df["priceDiffPercentage"])

    def get_ordinary_least_squares(self, linear_model, stock_data: pd.DataFrame, stock_prices: pd.Series):
        linear_model.fit(stock_data, stock_prices)
        coefficients = linear_model.coef_

        # gathers linear model coefficients
        linear_model_coef = {}
        for stock_report_column, stock_report_coef in zip(stock_data.columns, coefficients):
            linear_model_coef[stock_report_column] = stock_report_coef
        return linear_model_coef

