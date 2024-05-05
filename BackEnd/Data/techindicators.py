import pandas as pd

from BackEnd import constants
from BackEnd.Data.api import get_raw_api_data


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
            "MACD": f'https://www.alphavantage.co/query?function={self.ticker}&symbol=IBM&interval=daily&series_type=open&apikey={constants.API_KEY}',

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

        # getting all technical indicators name to dict
        for indicator_name, content in indicator_raw_data.items():
            technical_indicator_dfs[indicator_name] = pd.DataFrame([content["Meta Data"]], index=[0])
            for date, data in content[f"Technical Analysis: {indicator_name}"]:
                technical_indicator_dfs

        for indicator_name, raw_data_dicts in indicator_raw_data.items():
            for indicator_content, indicator_data_dict in raw_data_dicts.items():
                for column, data in indicator_data_dict.items():
                    technical_indicator_dfs[indicator_name] = pd.DataFrame({})
