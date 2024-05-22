import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler

from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.techindicators import TechnicalIndicators


class LinearModelFit(BaseModel):
    stock_ticker: str
    train_data: dict
    target_data: dict


def linear_model_eps_calender_fit(calender_df):
    linear_model_fit = []
    for report in calender_df.upcoming_earnings_calender_df.itertuples():
        company_data = CompanyData(ticker=report.symbol)
        technical_analysis = TechnicalIndicators(ticker=report.symbol)
        raw_stock_data_df = pd.DataFrame({
            "estimatedEPS": company_data.company_dfs.eps_df["estimatedEPS"],
            "SMA": technical_analysis.technical_indicator_data["SMA"]["SMA"],
            "EMA": technical_analysis.technical_indicator_data["EMA"]["EMA"],
            "RSI": technical_analysis.technical_indicator_data["RSI"]["RSI"],
            "MACD": technical_analysis.technical_indicator_data["MACD"]["MACD"],
            "BBANDSLower": technical_analysis.technical_indicator_data["BBANDS"]["lowerBound"],
            "BBANDSMiddle": technical_analysis.technical_indicator_data["BBANDS"]["middleBound"],
            "BBANDSUpper": technical_analysis.technical_indicator_data["BBANDS"]["upperBound"],
            "ADX": technical_analysis.technical_indicator_data["ADX"]["ADX"],
            "AD": technical_analysis.technical_indicator_data["AD"]["AD"],
            "OBV": technical_analysis.technical_indicator_data["OBV"]["OBV"]
        }).dropna()

        target_data_df = pd.DataFrame({
            "estimatedEPS": calender.estimatedEPS,
            "SMA": technical_analysis.technical_indicator_data["SMA"]["SMA"].mean(),
            "EMA": technical_analysis.technical_indicator_data["EMA"]["EMA"].mean(),
            "RSI": technical_analysis.technical_indicator_data["RSI"]["RSI"].mean(),
            "MACD": technical_analysis.technical_indicator_data["MACD"]["MACD"].mean(),
            "BBANDSLower": technical_analysis.technical_indicator_data["BBANDS"]["lowerBound"].mean(),
            "BBANDSMiddle": technical_analysis.technical_indicator_data["BBANDS"]["middleBound"].mean(),
            "BBANDSUpper": technical_analysis.technical_indicator_data["BBANDS"]["upperBound"].mean(),
            "ADX": technical_analysis.technical_indicator_data["ADX"]["ADX"].mean(),
            "AD": technical_analysis.technical_indicator_data["AD"]["AD"].mean(),
            "OBV": technical_analysis.technical_indicator_data["OBV"]["OBV"].mean()
        })

        linear_model_fit.append(LinearModelFit(train_data=raw_stock_data_df, target_data_df=target_data_df, stock_ticker=calender.symbol))
    return linear_model_fit


def linear_model_fit(stock_data, technical_indicators_data, estimatedEPS) -> dict:
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
    linear_model_df = data_scaler.fit_transform(X=raw_stock_data_df)

    # convert the linear model to a dataframe
    linear_model_df = pd.DataFrame(linear_model_df)

    # set columns of the df
    linear_model_df.columns = raw_stock_data_df.columns

    # drop the price differences from scale
    linear_model_stock_prices = linear_model_df["priceChange"]
    linear_model_df = linear_model_df.drop(columns="priceChange")

    formatted_data["stock_data"] = linear_model_df
    formatted_data["stock_prices"] = linear_model_stock_prices
    formatted_data["estimatedEPS"] = estimatedEPS

    return formatted_data
