from typing import Optional
import pandas as pd
import requests



def endpoint_company_request(ticker: Optional[str], api_key: Optional[str] = None) -> dict:
    dict_functions_company_urls = {
        "times_series_data": f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}",
        "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}",
        "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}",
        "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}",
        "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={api_key}",
        "earnings": f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={api_key}"
    }
    return dict_functions_company_urls


def endpoint_micro_request(ticker: Optional[str], api_key: Optional[str] = None) -> dict:
    dict_functions_micro_urls = {
        "real_gdp": f"https://www.alphavantage.co/query?function=REAL_GDP&symbol={ticker}&apikey={api_key}",
        "cpi": f"https://www.alphavantage.co/query?function=CPI&symbol={ticker}&apikey={api_key}",
        "inflation": f"https://www.alphavantage.co/query?function=INFLATION&symbol={ticker}&apikey={api_key}",
        "federal_funds_rate": f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&symbol={ticker}&apikey={api_key}",
        "retail_sales": f"https://www.alphavantage.co/query?function=RETAIL_SALES&symbol={ticker}&apikey={api_key}",
        "unemployment": f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&symbol={ticker}&apikey={api_key}"
    }
    return dict_functions_micro_urls


def get_raw_api_data(endpoints: dict) -> dict:
    raw_data = {}
    for data_description, endpoint_url in endpoints.items():
        raw_data[data_description] = requests.get(url=endpoint_url).json()
    return raw_data


def get_spec_api_data(raw_data: dict) -> dict:
    spec_data = {}
    spec_data["Current Date"] = raw_data["times_series_data"]["Meta Data"]["3. Last Refreshed"]
    spec_data["Current Price"] = raw_data["times_series_data"]["Time Series (Daily)"][spec_data["Current Date"]]["4. close"]
    spec_data["Volume"] = raw_data["times_series_data"]["Time Series (Daily)"][spec_data["Current Date"]]["5. volume"]
    spec_data["Ticker Symbol"] = raw_data["overview"]["Symbol"]
    spec_data["Company Description"] = raw_data["overview"]["Description"]
    spec_data["Market Cap"] = raw_data["overview"]["MarketCapitalization"]
    spec_data["52 Week High"] = raw_data["overview"]["52WeekHigh"]
    spec_data["52 Week Low"] = raw_data["overview"]["52WeekLow"]
    spec_data["Latest Quarter Date"] = raw_data["earnings"]["quarterlyEarnings"][000]["reportedDate"]
    spec_data["Reported EPS"] = raw_data["earnings"]["quarterlyEarnings"][000]["reportedEPS"]
    spec_data["Estimated EPS"] = raw_data["earnings"]["quarterlyEarnings"][000]["estimatedEPS"]
    spec_data["Revenue"] = raw_data["income_statement"]["quarterlyReports"][00]["totalRevenue"]
    spec_data["Profit"] = raw_data["income_statement"]["quarterlyReports"][00]["grossProfit"]

    return spec_data


def get_html(spec_data: dict) -> str:
    html = pd.DataFrame([spec_data]).to_html()
    return html

