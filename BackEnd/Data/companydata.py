import pandas as pd

from BackEnd.API.api import get_raw_api_data, get_company_endpoints, get_company_raw_data


class CompanyData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        endpoints = get_company_endpoints(ticker=self.ticker)
        raw_data_dict = get_raw_api_data(endpoints=endpoints)
        company_data = get_company_raw_data(company_raw_data=raw_data_dict)
        self.company_overview = company_data.company_overview
        self.company_dfs = CompanyDataDFS(company_data=company_data)


class CompanyDataDFS:
    def __init__(self, company_data):
        self.cashflow_df = get_company_cashflow_df(cashflow_data=company_data.company_cashflow)
        self.eps_df = get_company_eps_df(eps_data=company_data.company_eps)
        self.stock_data_df = get_company_stock_data(company_stock=company_data.company_prices)
        self.income_statement = get_company_income_statement_df(income_statement=company_data.company_income_statement)


def get_company_cashflow_df(cashflow_data) -> pd.DataFrame:
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

    return cashflow_df


def get_company_eps_df(eps_data):
    reported_date = []
    estimated_eps = []
    reported_eps = []
    surprise_percentage = []
    for eps_statement in eps_data:
        reported_date.append(eps_statement.reported_date)
        estimated_eps.append(eps_statement.estimated_eps)
        reported_eps.append(eps_statement.reported_eps)
        surprise_percentage.append(eps_statement.surprise_percentage)

    eps_df = pd.DataFrame({
        "reportedDate": reported_date,
        "estimatedEPS": estimated_eps,
        "reportedEPS": reported_eps,
        "surprisePercentage": surprise_percentage
    })

    return eps_df


def get_company_income_statement_df(income_statement):
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

    return income_statement_dfs


def get_company_stock_data(company_stock):
    close_prices = []
    high_prices = []
    low_prices = []
    volume = []
    for stock_data in company_stock:
        close_prices.append(stock_data.close)
        high_prices.append(stock_data.high)
        low_prices.append(stock_data.low)
        volume.append(stock_data.volume)

    stock_data_df = pd.DataFrame({
        "low": low_prices,
        "high": high_prices,
        "close": close_prices,
        "volume": volume
    })

    return stock_data_df
