import pandas as pd
from sklearn import linear_model

from BackEnd.Models.modelPrep import DataFit


def format_data_for_model(stock_report):
    formatted_df = pd.merge(stock_report.report_balance_sheet_differences_df, stock_report.report_eps_differences_df, left_index=True, right_index=True)
    formatted_df = formatted_df.drop(columns=["reportedDate_x", "reportedDate_y"])
    return formatted_df


class LinearModels:
    def __init__(self, model_data: type(DataFit)):
        self.model_data = model_data
        self.regr_model = linear_model.LinearRegression()
        self.least_ordinary_squares = self.get_ordinary_least_squares(linear_model=self.regr_model, pre_linear_model_data=model_data)

    def get_ordinary_least_squares(self, linear_model, pre_linear_model_data: dict):
        linear_model.fit(pre_linear_model_data["stock_data"], pre_linear_model_data["stock_prices"])
        coefficients = linear_model.coef_

        # gathers linear model coefficients
        linear_model_coef = {}
        for stock_report_column, stock_report_coef in zip(pre_linear_model_data["stock_data"].columns, coefficients):
            linear_model_coef[stock_report_column] = stock_report_coef
        return linear_model_coef

    def get_ridge_regression(self):
        pass
