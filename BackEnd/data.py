from typing import Optional

import requests
from bs4 import BeautifulSoup

def get_scraper(url: str):
    response = requests.get(url)
    scraper = BeautifulSoup(response.content, "html.parser")
    return scraper

def endpoint_company_request(api_key: Optional[str]=None):
    dict_functions_company_urls = {
        "times_series_data": f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}",
        "news_sentiment": f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol=IBM&apikey={api_key}",
        "top_gainers_losers": f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&symbol=IBM&apikey={api_key}" ,
        "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey={api_key}",
        "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey={api_key}",
        "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey={api_key}",
        "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey={api_key}",
        "earnings": f"https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey={api_key}"
    }
    return dict_functions_company_urls

def endpoint_micro_request(api_key: Optional[str]=None):
    dict_functions_micro_urls = {
        "real_gdp": f"https://www.alphavantage.co/query?function=REAL_GDP&symbol=IBM&apikey={api_key}",
        "cpi": f"https://www.alphavantage.co/query?function=CPI&symbol=IBM&apikey={api_key}",
        "inflation": f"https://www.alphavantage.co/query?function=INFLATION&symbol=IBM&apikey={api_key}",
        "federal_funds_rate": f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&symbol=IBM&apikey={api_key}",
        "retail_sales": f"https://www.alphavantage.co/query?function=RETAIL_SALES&symbol=IBM&apikey={api_key}",
        "unemployment": f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&symbol=IBM&apikey={api_key}"
    }
    return dict_functions_micro_urls

def get_api_data(endpoints: dict):
    api_data = {}
    for function, endpoint_url in endpoints.items():
        api_data[function] = requests.get(url=endpoint_url)
    return api_data
