import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from BackEnd.Data.earningsdata import EarningsData
from BackEnd.Data.microdata import MicroData


class DataFit:
    def __init__(self, stock_data):
        self.stock_data = stock_data
        earnings_data = EarningsData(stock_data=stock_data)
        micro_data = MicroData()
        self.linear_model_dict = self.linear_model_fit(stock_data=earnings_data, technical_indicators_data=earnings_data.technical_analysis_data_dfs, micro_data=micro_data.micro_df_data)

    def linear_model_fit(self, stock_data, technical_indicators_data, micro_data) -> dict:
        formatted_data = {}

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
            "priceChange": stock_data.report_prices_differences_df["priceDiffPercentage"],
            "SMA": technical_indicators_data["SMA"]["SMA"],
            "EMA": technical_indicators_data["EMA"]["EMA"],
            "RSI": technical_indicators_data["RSI"]["RSI"],
            "MACD": technical_indicators_data["MACD"]["MACD"],
            "BBANDSLower": technical_indicators_data["BBANDS"]["lowerBound"],
            "BBANDSMiddle": technical_indicators_data["BBANDS"]["middleBound"],
            "BBANDSUpper": technical_indicators_data["BBANDS"]["upperBound"],
            "ADX": technical_indicators_data["ADX"]["ADX"],
            "AD": technical_indicators_data["AD"]["AD"],
            "OBV": technical_indicators_data["OBV"]["OBV"]
        }).dropna()

        # find what the length of the df should be so that cash flow and eps data are all shows without na or 0 and flips df
        df_length = min(len(stock_data.report_eps_differences_df.index), len(stock_data.report_balance_sheet_differences_df.index))
        raw_stock_data_df = raw_stock_data_df[:df_length][::-1]

        # fill na and infinity values with 0
        raw_stock_data_df = raw_stock_data_df.replace(to_replace=[np.inf, -np.inf], value=0)

        # scale data to be ready to be processed
        data_scaler = StandardScaler()
        linear_model_df = data_scaler.fit_transform(raw_stock_data_df)

        # convert the linear model to a dataframe
        linear_model_df = pd.DataFrame(linear_model_df)

        # set columns of the df
        linear_model_df.columns = raw_stock_data_df.columns

        # drop the price differences from scale
        linear_model_stock_prices = linear_model_df["priceChange"]
        linear_model_df = linear_model_df.drop(columns="priceChange")

        formatted_data["stock_data"] = linear_model_df
        formatted_data["stock_prices"] = linear_model_stock_prices

        return formatted_data
