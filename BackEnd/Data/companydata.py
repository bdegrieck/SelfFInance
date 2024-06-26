from typing import List

import pandas as pd

from BackEnd.API.api import get_raw_api_data, get_company_endpoints, get_company_raw_data
from BackEnd.API.companyrawdata import CompanyRawData, CompanyCashFlow, CompanyEPS, CompanyIncomeStatement, \
    TimeSeriesData
from BackEnd.routines import merge


class CompanyData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        endpoints = get_company_endpoints(ticker=self.ticker)
        raw_data_dict = get_raw_api_data(endpoints=endpoints)
        company_data = get_company_raw_data(company_raw_data=raw_data_dict)
        self.company_overview = company_data.company_overview
        self.company_dfs = CompanyDataDFS(company_data=company_data)
        self.report_dates=self.company_dfs.eps_df["reportedDate"]


class CompanyDataDFS:
    def __init__(self, company_data: CompanyRawData):
        self.eps_df = get_company_eps_df(eps_data=company_data.company_eps)
        self.stock_data_df = get_company_stock_data(company_stock=company_data.company_prices)
        income_statement = get_company_income_statement_df(income_statement=company_data.company_income_statement)
        cashflow_df = get_company_cashflow_df(cashflow_data=company_data.company_cashflow)
        self.balance_sheet_df = get_balance_sheet(cashflow=cashflow_df, income_statement=income_statement)



def get_company_cashflow_df(cashflow_data: List[CompanyCashFlow]) -> pd.DataFrame:
    quarter_dates = []
    cashflow_from_financing = []
    cashflow_from_investment = []
    cashflow_from_operations = []
    for cashflow_statement in cashflow_data:
        quarter_dates.append(cashflow_statement.quarter_date)
        cashflow_from_financing.append(cashflow_statement.cashflow_from_financing)
        cashflow_from_investment.append(cashflow_statement.cashflow_from_investment)
        cashflow_from_operations.append(cashflow_statement.cashflow_from_operations)

    cashflow_df = pd.DataFrame({
        "quarterDate": quarter_dates,
        "cashFlowFromFinancing": cashflow_from_financing,
        "cashFlowFromInvestment": cashflow_from_investment,
        "cashFlowFromOperations": cashflow_from_operations
    })

    cashflow_df = cashflow_df.dropna().set_index("quarterDate")

    # calculates cash flow
    cashflow_df["cashFlow"] = cashflow_df["cashFlowFromFinancing"] + cashflow_df["cashFlowFromInvestment"] + cashflow_df["cashFlowFromOperations"]

    return cashflow_df


def get_company_eps_df(eps_data: List[CompanyEPS]) -> pd.DataFrame:
    reported_date = []
    estimated_eps = []
    reported_eps = []
    surprise_percentage = []
    quarter_dates = []
    for eps_statement in eps_data:
        quarter_dates.append(eps_statement.quarter_date)
        reported_date.append(eps_statement.reported_date)
        estimated_eps.append(eps_statement.estimated_eps)
        reported_eps.append(eps_statement.reported_eps)
        surprise_percentage.append(eps_statement.surprise_percentage)

    eps_df = pd.DataFrame({
        "quarterDate": quarter_dates,
        "reportedDate": reported_date,
        "estimatedEPS": estimated_eps,
        "reportedEPS": reported_eps,
        "surprisePercentage": surprise_percentage
    })

    eps_df = eps_df.dropna().set_index("quarterDate")

    return eps_df


def get_company_income_statement_df(income_statement: List[CompanyIncomeStatement]) -> pd.DataFrame:
    quarter_dates = []
    profit = []
    revenue = []

    for income_statement_report in income_statement:
        quarter_dates.append(income_statement_report.quarter_date)
        profit.append(income_statement_report.profit)
        revenue.append(income_statement_report.revenue)

    income_statement_dfs = pd.DataFrame({
        "quarterDates": quarter_dates,
        "profit": profit,
        "revenue": revenue
    })

    income_statement_dfs = income_statement_dfs.dropna().set_index("quarterDates")

    return income_statement_dfs


def get_company_stock_data(company_stock: List[TimeSeriesData]) -> pd.DataFrame:
    dates = []
    close_prices = []
    high_prices = []
    low_prices = []
    volume = []
    splits = []
    for stock_data in company_stock:
        dates.append(stock_data.date)
        close_prices.append(stock_data.close)
        high_prices.append(stock_data.high)
        low_prices.append(stock_data.low)
        volume.append(stock_data.volume)
        splits.append(stock_data.split)

    stock_data_df = pd.DataFrame({
        "date": dates,
        "low": low_prices,
        "high": high_prices,
        "close": close_prices,
        "volume": volume,
        "split": splits
    })

    stock_data_df = stock_data_df.dropna().set_index("date")

    # Calculate the cumulative product of the splits
    stock_data_df['splitSum'] = stock_data_df['split'].cumprod()

    # Adjust the 'low', 'high', and 'close' columns
    stock_data_df['low'] = stock_data_df['low'] / stock_data_df['splitSum']
    stock_data_df['high'] = stock_data_df['high'] / stock_data_df['splitSum']
    stock_data_df['close'] = stock_data_df['close'] / stock_data_df['splitSum']

    # Drop the 'split_sum' column if you don't need it anymore
    stock_data_df.drop(columns=['splitSum'], inplace=True)

    return stock_data_df


def get_balance_sheet(cashflow: pd.DataFrame, income_statement: pd.DataFrame) -> pd.DataFrame:
    balance_sheet = merge(cashflow, income_statement)
    return balance_sheet
