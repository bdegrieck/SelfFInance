import pandas as pd
from BackEnd import constants
import requests
from BackEnd.Data.api import get_earnings_calender_endpoints, get_raw_api_csv_dfs, get_calender_dfs
import datetime as dt


def get_market_cap(ticker: str):
    try:
        market_cap_endpoint = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={constants.API_KEY}"
        market_cap_raw = requests.get(url=market_cap_endpoint).json()
        market_cap = float(market_cap_raw["MarketCapitalization"])
    except:
        return None
    return market_cap


class EarningsCalender:

    def __init__(self, ticker: str):
        endpoints = get_earnings_calender_endpoints(ticker=ticker)
        raw_data = get_raw_api_csv_dfs(endpoints=endpoints)
        calender_dfs = get_calender_dfs(raw_data=raw_data)
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
        big_companies = []
        for ticker in calender_df["symbol"]:
            market_cap = get_market_cap(ticker=ticker)
            if market_cap is not None and market_cap >= 1000000000:
                big_companies.append(ticker)

        calender_df = calender_df[calender_df["symbol"].isin(big_companies)].reset_index(drop=True)

        return calender_df[["symbol", "reportDate", "fiscalDateEnding", "estimate"]]

    def get_company_earnings_calender(self, calender_df: pd.DataFrame):

        # return earnings calendar for a single company and drop unknown report dates

        # set dates to date
        calender_df["reportDate"] = calender_df["reportDate"].dt.date
        calender_df["fiscalDateEnding"] = calender_df["fiscalDateEnding"].dt.date

        return calender_df[["symbol", "reportDate", "fiscalDateEnding", "estimate"]].dropna()
