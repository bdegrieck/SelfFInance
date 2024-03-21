from typing import Optional

from BackEnd import constants
from BackEnd.data import get_raw_api_data, get_html
import pandas as pd


class MicroData:
    def __init__(self):
        self.api_key = constants.API_KEY
        self.ticker = "AAPL"
        self.micro_endpoints = self.get_endpoint_micro()
        self.micro_raw_data = get_raw_api_data(endpoints=self.micro_endpoints)
        self.micro_df_data = self.get_micro_df_data()
        self.micro_html_data = get_html(self.micro_df_data)

    def get_endpoint_micro(self) -> dict:
        dict_functions_micro_urls = {
            "real_gdp": f"https://www.alphavantage.co/query?function=REAL_GDP&symbol={self.ticker}&apikey={self.api_key}",
            "cpi": f"https://www.alphavantage.co/query?function=CPI&symbol={self.ticker}&apikey={self.api_key}",
            "inflation": f"https://www.alphavantage.co/query?function=INFLATION&symbol={self.ticker}&apikey={self.api_key}",
            "federal_funds_rate": f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&symbol={self.ticker}&apikey={self.api_key}",
            "retail_sales": f"https://www.alphavantage.co/query?function=RETAIL_SALES&symbol={self.ticker}&apikey={self.api_key}",
            "unemployment": f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&symbol={self.ticker}&apikey={self.api_key}"
        }
        return dict_functions_micro_urls

    # format raw data to specific returns a dictionary of dfs
    def get_micro_df_data(self) -> dict:
        micro_dfs = {
            "real_gdp_df": pd.DataFrame(self.micro_raw_data["real_gdp"]["data"]).set_index("date").astype(float).rename(columns={"value": "Real GDP"}),
            "cpi_df": pd.DataFrame(self.micro_raw_data["cpi"]["data"]).set_index("date").astype(float).rename(columns={"value": "CPI"}),
            "inflation_df": pd.DataFrame(self.micro_raw_data["inflation"]["data"]).set_index("date").astype(float).rename(columns={"value": "Inflation"}),
            "federal_funds_rate_df": pd.DataFrame(self.micro_raw_data["federal_funds_rate"]["data"]).set_index("date").astype(float).rename(columns={"value": "Federal Funds Rate"}),
            "retail_sales_df": pd.DataFrame(self.micro_raw_data["retail_sales"]["data"]).set_index("date").astype(float).rename(columns={"value": "Retail Sales"}),
            "unemployment_rate_df": pd.DataFrame(self.micro_raw_data["unemployment"]["data"]).set_index("date").astype(float).rename(columns={"value": "Unemployment Rate"}),
        }
        return micro_dfs
