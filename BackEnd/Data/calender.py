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
        calender_raw_data = get_calender_raw_data(raw_data=raw_data)
        company_earnings_df = get_company_earnings_df(calender_raw_data=calender_raw_data.company_earnings_calendar)
        upcoming_earnings_df = get_upcoming_earnings_calender_df(calender_raw_data=calender_raw_data.upcoming_earnings_calendar)
        self.upcoming_earnings_calender_df = self.get_sorted_companies_calender(calender_df=upcoming_earnings_df)
        self.upcoming_earnings_calender_company_df = self.get_company_earnings_calender(calender_df=company_earnings_df)

    def get_sorted_companies_calender(self, calender_df: pd.DataFrame):

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


def get_company_earnings_df(calender_raw_data):
    quarter_dates = []
    eps_estimates = []
    report_dates = []

    for earning_report in calender_raw_data:
        quarter_dates.append(earning_report.quarter_date)
        eps_estimates.append(earning_report.eps_estimate)
        report_dates.append(earning_report.report_date)

    company_earnings_df = pd.DataFrame({
        "quarterDate": quarter_dates,
        "reportDate": report_dates,
        "epsEstimate": eps_estimates
    })

    company_earnings_df = company_earnings_df.dropna().set_index("quarterDate")

    return company_earnings_df


def get_upcoming_earnings_calender_df(calender_raw_data):
    quarter_dates = []
    report_dates = []
    company_names = []
    symbols = []
    currencies = []
    eps_estimates = []

    for earnings_report in calender_raw_data:
        quarter_dates.append(earnings_report.quarter_date)
        report_dates.append(earnings_report.report_date)
        company_names.append(earnings_report.company_name)
        symbols.append(earnings_report.symbol)
        currencies.append(earnings_report.currency)
        eps_estimates.append(earnings_report.eps_estimate)

    upcoming_earnings = pd.DataFrame({
        "quarterDate": quarter_dates,
        "reportDate": report_dates,
        "companyName": company_names,
        "ticker": symbols,
        "epsEstimate": eps_estimates,
        "currency": currencies
    })

    upcoming_earnings = upcoming_earnings.dropna().set_index("quarterDate").drop(columns="currency").sort_values(by="reportDate")

    return upcoming_earnings

