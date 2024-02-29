from typing import Optional
import pandas as pd
import requests



# format company endpoints
def get_endpoint_company(ticker: Optional[str], api_key: Optional[str] = None) -> dict:
    dict_functions_company_urls = {
        "times_series_data": f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}",
        "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}",
        "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}",
        "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}",
        "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={api_key}",
        "earnings": f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={api_key}"
    }
    return dict_functions_company_urls


# format micro endpoints
def get_endpoint_micro(ticker: Optional[str], api_key: Optional[str] = None) -> dict:
    dict_functions_micro_urls = {
        "real_gdp": f"https://www.alphavantage.co/query?function=REAL_GDP&symbol={ticker}&apikey={api_key}",
        "cpi": f"https://www.alphavantage.co/query?function=CPI&symbol={ticker}&apikey={api_key}",
        "inflation": f"https://www.alphavantage.co/query?function=INFLATION&symbol={ticker}&apikey={api_key}",
        "federal_funds_rate": f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&symbol={ticker}&apikey={api_key}",
        "retail_sales": f"https://www.alphavantage.co/query?function=RETAIL_SALES&symbol={ticker}&apikey={api_key}",
        "unemployment": f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&symbol={ticker}&apikey={api_key}"
    }
    return dict_functions_micro_urls


# get raw data endpoints are passed in
def get_raw_api_data(endpoints: dict) -> dict:
    raw_data = {}
    for data_description, endpoint_url in endpoints.items():
        raw_data[data_description] = requests.get(url=endpoint_url).json()
    return raw_data


# format raw data to specific data returns a dictionary of dfs
def get_company_df_data(raw_company_data: dict) -> dict:
    company_dfs = {}
    company_dfs["ticker_prices_df"] = pd.DataFrame(raw_company_data["times_series_data"]["Time Series (Daily)"]).transpose()
    company_dfs["ticker_overview_df"] = pd.DataFrame({
        "Ticker Symbol": [raw_company_data["overview"]["Symbol"]],
        "Company Description": [raw_company_data["overview"]["Description"]],
        "Market Cap": [raw_company_data["overview"]["MarketCapitalization"]],
        "52 Week High": [raw_company_data["overview"]["52WeekHigh"]],
        "52 Week Low": [raw_company_data["overview"]["52WeekLow"]]
    })
    company_dfs["ticker_eps_df"] = pd.DataFrame(raw_company_data["earnings"]["quarterlyEarnings"])
    company_dfs["ticker_balance_df"]= pd.DataFrame({
        "Date": pd.DataFrame(raw_company_data["income_statement"]["quarterlyReports"])["fiscalDateEnding"],
        "Total Revenue": pd.DataFrame(raw_company_data["income_statement"]["quarterlyReports"])["totalRevenue"],
        "Profit": pd.DataFrame(raw_company_data["income_statement"]["quarterlyReports"])["totalRevenue"]
    })
    return company_dfs


# format raw data to specific returns a dictionary of dfs
def get_micro_df_data(raw_micro_data: dict) -> dict:
    micro_dfs = {}
    micro_dfs["real_gdp_df"] = pd.DataFrame(raw_micro_data["real_gdp"]["data"])
    micro_dfs["cpi_df"] = pd.DataFrame(raw_micro_data["cpi"]["data"])
    micro_dfs["inflation_df"] = pd.DataFrame(raw_micro_data["inflation"]["data"])
    micro_dfs["federal_funds_df"] = pd.DataFrame(raw_micro_data["federal_funds_rate"]["data"])
    micro_dfs["retail_funds_df"] = pd.DataFrame(raw_micro_data["retail_sales"]["data"])
    micro_dfs["unemployment_df"] = pd.DataFrame(raw_micro_data["unemployment"]["data"])
    return micro_dfs


# format spec data dfs to html to frontend
def get_html(df_data: dict) -> dict:
    html_data = {}
    for df, data in df_data.items():
        html_data[df] = data.to_html()
    return html_data


# sends df data to flask template
# def render_data(html_data: str):
#     return post_data(data=html_data)
