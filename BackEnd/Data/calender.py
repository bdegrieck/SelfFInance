import datetime as dt
from functools import lru_cache

import pandas as pd
import requests

from BackEnd import constants
from BackEnd.API.api import get_earnings_calender_endpoints, get_raw_api_csv_dfs, get_calender_raw_data


@lru_cache(maxsize=1000)
def get_market_cap(ticker: str):
    try:
        market_cap_endpoint = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={constants.API_KEY}"
        response = requests.get(url=market_cap_endpoint)
        response.raise_for_status()
        market_cap = float(response.json()["MarketCapitalization"])
    except (requests.exceptions.HTTPError, KeyError, ValueError):
        return None
    return market_cap


class EarningsCalender:

    def __init__(self, ticker: str):
        endpoints = get_earnings_calender_endpoints(ticker=ticker)
        raw_data = get_raw_api_csv_dfs(endpoints=endpoints)
        calender_dfs = get_calender_raw_data(raw_data=raw_data)
        self.upcoming_earnings_calender_df = self.get_sorted_companies_calender(calender_df=calender_dfs["upcoming_earnings_calender"])
        self.upcoming_earnings_calender_company_df = self.get_company_earnings_calender(calender_df=calender_dfs["company_earnings_calender"])

    def get_sorted_companies_calender(self, calender_df: pd.DataFrame):

        # gets today's date and ranges a week so df is smaller
        todays_date = dt.datetime.today()
        next_date = todays_date + dt.timedelta(days=2)

        # reformat calendar that filters U.S companies, sorts the report Dates and drops empty rows and only a week range
        calender_df = calender_df[
            (calender_df["currency"] == "USD") &
            (calender_df["symbol"].str.len() <= 4) &
            ((calender_df["reportDate"] >= todays_date) & (calender_df["reportDate"] <= next_date))
        ].sort_values(by="reportDate").dropna()

        # set dates to date
        calender_df["reportDate"] = calender_df["reportDate"].dt.date
        calender_df["fiscalDateEnding"] = calender_df["fiscalDateEnding"].dt.date

        # filters out df with companies with market caps greater than 1 billion
        # calender_df["marketCap"] = calender_df["symbol"].apply(get_market_cap)
        # calender_df = calender_df[calender_df["marketCap"] > 1e9].reset_index(drop=True)

        return calender_df[["symbol", "name", "reportDate", "fiscalDateEnding", "estimate"]]

    def get_company_earnings_calender(self, calender_df: pd.DataFrame):

        # set dates to date
        calender_df["reportDate"] = calender_df["reportDate"].dt.date
        calender_df["fiscalDateEnding"] = calender_df["fiscalDateEnding"].dt.date

        return calender_df[["symbol", "reportDate", "fiscalDateEnding", "estimate"]].dropna()
