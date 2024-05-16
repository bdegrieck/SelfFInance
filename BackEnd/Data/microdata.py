import pandas as pd
from typing import List

from BackEnd.API.api import get_raw_api_data, get_micro_endpoints, get_micro_raw_data
from BackEnd.API.microrawdata import UnemploymentRates, RetailSales, InterestRates, InflationRates, CPI, RealGDP


class MicroData:
    def __init__(self):
        endpoints = get_micro_endpoints()
        raw_data = get_raw_api_data(endpoints=endpoints)
        micro_raw_data = get_micro_raw_data(raw_data=raw_data)
        self.real_gdp = get_real_gdp_df(real_gdp_data=micro_raw_data.real_gdp)
        self.cpi = get_cpi_df(cpi_data=micro_raw_data.cpi)
        self.inflation_rates = get_inflation_rate_df(inflation_rates_data=micro_raw_data.inflation_rates)
        self.interest_rates = get_interest_rates_df(interest_rates_data=micro_raw_data.interest_rates)
        self.retail_sales = get_retail_sales_df(retail_sales_data=micro_raw_data.retail_sales)
        self.unemployment_rates = get_unemployment_rate_df(unemployment_rate_data=micro_raw_data.unemployment_rates)


def get_real_gdp_df(real_gdp_data: List[RealGDP]) -> pd.DataFrame:
    dates = []
    real_gdp = []
    for real_gdp_report in real_gdp_data:
        dates.append(real_gdp_report.date)
        real_gdp.append(real_gdp_report.real_gdp)

    real_gdp_df = pd.DataFrame({
        "date": dates,
        "realGDP": real_gdp
    })

    real_gdp_df = real_gdp_df.dropna().set_index("date")

    return real_gdp_df


def get_cpi_df(cpi_data: List[CPI]) -> pd.DataFrame:
    dates = []
    cpi = []
    for cpi_report in cpi_data:
        dates.append(cpi_report.date)
        cpi.append(cpi_report.cpi)

    cpi_df = pd.DataFrame({
        "date": dates,
        "cpi": cpi
    })

    cpi_df = cpi_df.dropna().set_index("date")

    return cpi_df


def get_inflation_rate_df(inflation_rates_data: List[InflationRates]) -> pd.DataFrame:
    dates = []
    inflation_rates = []
    for inflation_rate_report in inflation_rates_data:
        dates.append(inflation_rate_report.date)
        inflation_rates.append(inflation_rate_report.inflation_rate)

    inflation_rate_df = pd.DataFrame({
        "date": dates,
        "inflationRate": inflation_rates
    })

    inflation_rate_df = inflation_rate_df.dropna().set_index("date")

    return inflation_rate_df


def get_interest_rates_df(interest_rates_data: List[InterestRates]) -> pd.DataFrame:
    dates = []
    interest_rates = []
    for interest_rates_report in interest_rates_data:
        dates.append(interest_rates_report.date)
        interest_rates.append(interest_rates_report.interest_rate)

    interest_rate_df = pd.DataFrame({
        "date": dates,
        "interestRate": interest_rates
    })

    interest_rate_df = interest_rate_df.dropna().set_index("date")

    return interest_rate_df


def get_retail_sales_df(retail_sales_data: List[RetailSales]) -> pd.DataFrame:
    dates = []
    retail_sales = []
    for retail_sales_report in retail_sales_data:
        dates.append(retail_sales_report.date)
        retail_sales.append(retail_sales_report.retail_sale)

    retail_sales_df = pd.DataFrame({
        "date": dates,
        "retailSales": retail_sales
    })

    retail_sales_df = retail_sales_df.dropna().set_index("date")

    return retail_sales_df


def get_unemployment_rate_df(unemployment_rate_data: List[UnemploymentRates]) -> pd.DataFrame:
    dates = []
    unemployment_rates = []
    for unemployment_rate_report in unemployment_rate_data:
        dates.append(unemployment_rate_report.date)
        unemployment_rates.append(unemployment_rate_report.unemployment_rate)

    unemployment_rate_df = pd.DataFrame({
        "date": dates,
        "unemploymentRate": unemployment_rates
    })

    unemployment_rate_df = unemployment_rate_df.dropna().set_index("date")

    return unemployment_rate_df
