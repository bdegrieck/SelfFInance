import pandas as pd

from BackEnd import constants
from BackEnd.Data.api import get_raw_api_data


def get_technical_analysis_values(tech_analysis_dict: dict, tech_analysis_name: str):
    technical_analysis_values = []
    for date, tech_analysis_dict_values in tech_analysis_dict.items():
        technical_analysis_values.append(float(tech_analysis_dict_values[tech_analysis_name]))
    return technical_analysis_values

def get_bbands_technical_analysis_values(tech_analysis_dict: dict):
    lower_bound_data = []
    middle_bound_data = []
    upper_bound_data = []

    for date, bbands_values in tech_analysis_dict.items():
        lower_bound_data.append(bbands_values["Real Lower Band"])
        middle_bound_data.append(bbands_values["Real Middle Band"])
        upper_bound_data.append(bbands_values["Real Upper Band"])

    return {
        "lowerBound": lower_bound_data,
        "middleBound": middle_bound_data,
        "upperBound": upper_bound_data,
    }


class TechnicalIndicators:

    def __init__(self, ticker: str):
        self.ticker = ticker
        endpoints = self.get_technical_indicator_endpoints()
        raw_data = get_raw_api_data(endpoints=endpoints)
        self.technical_indicator_data = self.get_technical_indicator_df_data(indicator_raw_data=raw_data)

    def get_technical_indicator_endpoints(self):
        endpoints = {
            # (Simple Moving Average) Averages the price over a specific period to identify trend directions
            "SMA": f'https://www.alphavantage.co/query?function=SMA&symbol={self.ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

            # (Exponential Moving Average) Similar to SMA but gives more weight to recent prices, making it more responsive to recent price changes
            "EMA": f'https://www.alphavantage.co/query?function=EMA&symbol={self.ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

            # (Relative Strength Index) A momentum indicator that measures the speed and change of price movements to identify overbought or oversold conditions
            "RSI": f'https://www.alphavantage.co/query?function=RSI&symbol={self.ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

            # (Moving Average Convergence Divergence): Measures the relationship between two moving averages to identify trends and momentum shifts
            "MACD": f'https://www.alphavantage.co/query?function=MACD&symbol={self.ticker}&interval=daily&series_type=open&apikey={constants.API_KEY}',

            # Bollinger Bands used to identify periods of high or low volatility based on moving averages
            "BBANDS": f'https://www.alphavantage.co/query?function=BBANDS&symbol={self.ticker}&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey={constants.API_KEY}',

            # (Average Directional Index): Measures the strength of a trend
            "ADX": f'https://www.alphavantage.co/query?function=ADX&symbol={self.ticker}&interval=daily&time_period=10&apikey={constants.API_KEY}',

            # (Accumulation/Distribution) Useful for determining the strength of trends by showing if price movements are supported by strong buying or selling pressure
            "AD": f'https://www.alphavantage.co/query?function=AD&symbol={self.ticker}&interval=daily&apikey={constants.API_KEY}',

            # (On-Balance Volume)  Often used as a leading indicator, suggesting potential trend reversals before price action confirms them
            "OBV": f'https://www.alphavantage.co/query?function=OBV&symbol={self.ticker}&interval=weekly&apikey={constants.API_KEY}'
        }
        return endpoints

    def get_technical_indicator_df_data(self, indicator_raw_data):
        technical_indicator_dfs = {}

        technical_indicator_dfs["SMA"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["SMA"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["SMA"][f"Technical Analysis: SMA"].keys()),
                "SMA": get_technical_analysis_values(
                    tech_analysis_dict=indicator_raw_data["SMA"]["Technical Analysis: SMA"],
                    tech_analysis_name="SMA"),
            }).set_index("date")
        }

        technical_indicator_dfs["EMA"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["EMA"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["EMA"][f"Technical Analysis: EMA"].keys()),
                "EMA": get_technical_analysis_values(
                    tech_analysis_dict=indicator_raw_data["EMA"]["Technical Analysis: EMA"],
                    tech_analysis_name="EMA"),
            }).set_index("date")
        }

        technical_indicator_dfs["RSI"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["RSI"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["RSI"][f"Technical Analysis: RSI"].keys()),
                "RSI": get_technical_analysis_values(
                    tech_analysis_dict=indicator_raw_data["RSI"]["Technical Analysis: RSI"],
                    tech_analysis_name="RSI"),
            }).set_index("date")
        }

        technical_indicator_dfs["MACD"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["MACD"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["MACD"][f"Technical Analysis: MACD"].keys()),
                "MACD": get_technical_analysis_values(
                    tech_analysis_dict=indicator_raw_data["MACD"]["Technical Analysis: MACD"],
                    tech_analysis_name="MACD"),
            }).set_index("date")
        }

        bbands_values = get_bbands_technical_analysis_values(tech_analysis_dict=indicator_raw_data["BBANDS"]["Technical Analysis: BBANDS"])

        technical_indicator_dfs["BBANDS"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["BBANDS"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["BBANDS"][f"Technical Analysis: BBANDS"].keys()),
                "lowerBound": bbands_values["lowerBound"],
                "middleBound": bbands_values["middleBound"],
                "upperBound": bbands_values["upperBound"],
            }).set_index("date")
        }

        technical_indicator_dfs["ADX"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["ADX"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["ADX"][f"Technical Analysis: ADX"].keys()),
                "ADX": get_technical_analysis_values(
                    tech_analysis_dict=indicator_raw_data["ADX"]["Technical Analysis: ADX"],
                    tech_analysis_name="ADX"),
            }).set_index("date")
        }

        technical_indicator_dfs["AD"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["AD"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["AD"][f"Technical Analysis: Chaikin A/D"].keys()),
                "AD": get_technical_analysis_values(
                    tech_analysis_dict=indicator_raw_data["AD"]["Technical Analysis: Chaikin A/D"],
                    tech_analysis_name="Chaikin A/D"),
            }).set_index("date")
        }

        technical_indicator_dfs["OBV"] = {
            "Meta Data": pd.DataFrame([indicator_raw_data["OBV"]["Meta Data"]]),
            "Technical Analysis Data": pd.DataFrame({
                "date": pd.DatetimeIndex(indicator_raw_data["OBV"][f"Technical Analysis: OBV"].keys()),
                "OBV": get_technical_analysis_values(
                    tech_analysis_dict=indicator_raw_data["OBV"]["Technical Analysis: OBV"],
                    tech_analysis_name="OBV"),
            }).set_index("date")
        }

        return technical_indicator_dfs
