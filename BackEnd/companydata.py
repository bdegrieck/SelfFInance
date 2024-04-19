import numpy as np
import pandas as pd

from BackEnd import constants
from BackEnd.api import API


class CompanyData:

    def __init__(self, ticker: str):
        self.raw_data = API(ticker=ticker)
        self.company_prices = self.raw_data.ticker_df_data["ticker_prices_df"]
        self.company_overview = self.raw_data.ticker_df_data["ticker_overview_df"]
        self.company_eps = self.raw_data.ticker_df_data["ticker_eps_df"]
        self.company_balance_sheet = self.raw_data.ticker_df_data["ticker_balance_df"]



