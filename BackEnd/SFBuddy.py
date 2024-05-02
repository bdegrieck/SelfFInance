import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from BackEnd.Data.companydata import CompanyData


class OrdinaryLeastSquares:
    def __init__(self, company: type(CompanyData)):
        self.stock_prices_prediction = None
        self.stock_prices_target = None
        self.regr_model = linear_model.LinearRegression()
        self.least_ordinary_squares = self.get_ordinary_least_squares(linear_model=self.regr_model, stock_data=company.company_report_differences)


    def get_ordinary_least_squares(self, linear_model, company_differentials: pd.DataFrame, user_stock_report_input: pd.DataFrame):
        stock_report = company_differentials[["estimatedEPS", "estimatedEPSDiffPercentage", "profit", "cashFlow"]]
        stock_prices = company_differentials["priceDiffPercentage"]
        linear_model.fit(stock_report, stock_prices)
        prices_guess = linear_model.predict(user_stock_report_input)

        linear_model_results = {
            "coefficients": linear_model.coef_
            "prices prediction":
        }

