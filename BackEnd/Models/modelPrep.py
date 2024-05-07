import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from BackEnd.Data.earningsdata import EarningsData
from BackEnd.Data.techindicators import TechnicalIndicators


class DataFit:
    def __init__(self, stock_data):
        self.stock_data = stock_data
        stock_differences = EarningsData(stock_data=stock_data)
        technical_indicators = TechnicalIndicators(ticker=stock_data.ticker)
        linear_model_df = self.linear_model_fit(stock_data=stock_differences)

    def linear_model_fit(self, stock_data):
        stock_data.report_balance_sheet_differences_df = stock_data.report_balance_sheet_differences_df[(stock_data.report_balance_sheet_differences_df != 0).all(axis=1)]

        raw_stock_data_df = pd.DataFrame({
            "estimatedEPS": stock_data.report_eps_differences_df["estimatedEPS"],
            "estimatedEPSDiff": stock_data.report_eps_differences_df["estimatedEPSDiffPercentage"],
            "reportedEPS": stock_data.report_eps_differences_df["reportedEPS"],
            "reportedEPSDiff": stock_data.report_eps_differences_df["reportedEPSDiffPercentage"],
            "surpriseEPS": stock_data.report_eps_differences_df["surprisePercentage"] / 100,
            "totalRevenue": stock_data.report_balance_sheet_differences_df["totalRevenue"],
            "totalRevenueDiff": stock_data.report_balance_sheet_differences_df["totalRevenueDiff"],
            "profit": stock_data.report_balance_sheet_differences_df["profit"],
            "profitDiff": stock_data.report_balance_sheet_differences_df["profitDiff"],
            "cashFlow": stock_data.report_balance_sheet_differences_df["cashFlow"],
            "cashFlowDiff": stock_data.report_balance_sheet_differences_df["cashFlowDiff"],
            "priceChange": stock_data.report_prices_differences_df["priceDiffPercentage"]
        })[::-1]

        # find what the length of the df should be so that cash flow and eps data are all shows without na or 0
        df_length = min(len(stock_data.report_eps_differences_df.index), len(stock_data.report_balance_sheet_differences_df.index))
        raw_stock_data_df = raw_stock_data_df[:df_length]

        # fill na and infinity values with 0
        raw_stock_data_df = raw_stock_data_df.replace(to_replace=[np.inf, -np.inf], value=0)

        # scale data to be ready to be processed
        data_scaler = StandardScaler()
        linear_model_df = data_scaler.fit_transform(raw_stock_data_df)

        return linear_model_df
