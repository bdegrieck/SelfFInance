import pandas as pd
import requests

from BackEnd import constants
from BackEnd.Data.dataclean import check_raw_data, get_technical_analysis_values, get_clean_data, remove_empties, \
    get_ticker_balance_df_adj, get_bbands_technical_analysis_values


# get raw data endpoints are passed in
def get_raw_api_data(endpoints: dict) -> dict:
    raw_data = {}
    for data_description, endpoint_url in endpoints.items():
        raw_data[data_description] = requests.get(url=endpoint_url).json()
    check_raw_data(ticker_raw_data=raw_data)
    return raw_data


# format company endpoints
def get_company_endpoints(ticker: str) -> dict:
    dict_functions_company_urls = {
        "times_series_data": f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={constants.API_KEY}&outputsize=full",
        "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={constants.API_KEY}",
        "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={constants.API_KEY}",
        "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={constants.API_KEY}",
        "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={constants.API_KEY}",
        "earnings": f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={constants.API_KEY}"
    }

    return dict_functions_company_urls


# formats micro endpoints returns dict of endpoints
def get_micro_endpoints() -> dict:
    dict_functions_micro_urls = {
        "real_gdp": f"https://www.alphavantage.co/query?function=REAL_GDP&symbol=AAPL&apikey={constants.API_KEY}",
        "cpi": f"https://www.alphavantage.co/query?function=CPI&symbol=AAPL&apikey={constants.API_KEY}",
        "inflation": f"https://www.alphavantage.co/query?function=INFLATION&symbol=AAPL&apikey={constants.API_KEY}",
        "federal_funds_rate": f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&symbol=AAPL&apikey={constants.API_KEY}",
        "retail_sales": f"https://www.alphavantage.co/query?function=RETAIL_SALES&symbol=AAPL&apikey={constants.API_KEY}",
        "unemployment": f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&symbol=AAPL&apikey={constants.API_KEY}"
    }
    return dict_functions_micro_urls


def get_technical_indicator_endpoints(ticker: str):
    endpoints = {
        # (Simple Moving Average) Averages the price over a specific period to identify trend directions
        "SMA": f'https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

        # (Exponential Moving Average) Similar to SMA but gives more weight to recent prices, making it more responsive to recent price changes
        "EMA": f'https://www.alphavantage.co/query?function=EMA&symbol={ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

        # (Relative Strength Index) A momentum indicator that measures the speed and change of price movements to identify overbought or oversold conditions
        "RSI": f'https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

        # (Moving Average Convergence Divergence): Measures the relationship between two moving averages to identify trends and momentum shifts
        "MACD": f'https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval=daily&series_type=open&apikey={constants.API_KEY}',

        # Bollinger Bands used to identify periods of high or low volatility based on moving averages
        "BBANDS": f'https://www.alphavantage.co/query?function=BBANDS&symbol={ticker}&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey={constants.API_KEY}',

        # (Average Directional Index): Measures the strength of a trend
        "ADX": f'https://www.alphavantage.co/query?function=ADX&symbol={ticker}&interval=daily&time_period=10&apikey={constants.API_KEY}',

        # (Accumulation/Distribution) Useful for determining the strength of trends by showing if price movements are supported by strong buying or selling pressure
        "AD": f'https://www.alphavantage.co/query?function=AD&symbol={ticker}&interval=daily&apikey={constants.API_KEY}',

        # (On-Balance Volume)  Often used as a leading indicator, suggesting potential trend reversals before price action confirms them
        "OBV": f'https://www.alphavantage.co/query?function=OBV&symbol={ticker}&interval=weekly&apikey={constants.API_KEY}'
    }
    return endpoints


# format raw data to specific data returns a dictionary of dfs
def get_company_df_data(company_raw_data: dict) -> dict:
    company_dfs = {}

    company_dfs["ticker_prices_df"] = pd.DataFrame(company_raw_data["times_series_data"]["Time Series (Daily)"]).transpose()
    company_dfs["ticker_prices_df"].columns = ["open", "high", "low", "adjustedClose", "close", "volume", "dividends", "splits"]
    company_dfs["ticker_prices_df"] = company_dfs["ticker_prices_df"][["open", "high", "low", "close", "volume"]]
    company_dfs["ticker_prices_df"].index = pd.DatetimeIndex(company_dfs["ticker_prices_df"].index)

    company_dfs["ticker_overview_df"] = pd.DataFrame({
        "tickerSymbol": [company_raw_data["overview"]["Symbol"]],
        "companyDescription": company_raw_data["overview"]["Description"],
        "marketCap": company_raw_data["overview"]["MarketCapitalization"],
        "52weekHigh": company_raw_data["overview"]["52WeekHigh"],
        "52weekLow": company_raw_data["overview"]["52WeekLow"]
    })

    company_dfs["ticker_eps_df"] = pd.DataFrame(company_raw_data["earnings"]["quarterlyEarnings"]).set_index("fiscalDateEnding")[["estimatedEPS", "reportedEPS", "surprisePercentage", "reportedDate"]]
    company_dfs["ticker_eps_df"].index = pd.DatetimeIndex(company_dfs["ticker_eps_df"].index)
    company_dfs["ticker_eps_df"]["reportedDate"] = pd.DatetimeIndex(company_dfs["ticker_eps_df"]["reportedDate"])

    company_dfs["ticker_balance_df"] = pd.DataFrame({
        "date": pd.DataFrame(company_raw_data["income_statement"]["quarterlyReports"])["fiscalDateEnding"],
        "totalRevenue": pd.DataFrame(company_raw_data["income_statement"]["quarterlyReports"])["totalRevenue"],
        "profit": pd.DataFrame(company_raw_data["income_statement"]["quarterlyReports"])["netIncome"],
        "operatingCashFlow": pd.DataFrame(company_raw_data["cash_flow"]["quarterlyReports"])["operatingCashflow"],
        "cashFlowFromFinancing": pd.DataFrame(company_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromFinancing"],
        "cashFlowFromInvestment": pd.DataFrame(company_raw_data["cash_flow"]["quarterlyReports"])["cashflowFromInvestment"],
        "reportedDate": pd.DataFrame(company_raw_data["earnings"]["quarterlyEarnings"])["reportedDate"]
    }).set_index("date")

    # settings dates to timestamps
    company_dfs["ticker_balance_df"].index = pd.DatetimeIndex(company_dfs["ticker_balance_df"].index)
    company_dfs["ticker_balance_df"]["reportedDate"] = pd.DatetimeIndex(company_dfs["ticker_balance_df"]["reportedDate"])

    # data cleanse
    company_dfs = get_clean_data(company_dfs)
    company_dfs = remove_empties(company_dfs)

    # calculates cash flow
    company_dfs["ticker_balance_df"] = get_ticker_balance_df_adj(company_dfs["ticker_balance_df"])

    return company_dfs


def get_micro_df_data(raw_data) -> dict:
    micro_dfs = {
        "real_gdp_df": pd.DataFrame(raw_data["real_gdp"]["data"]).set_index("date").astype(float).rename(columns={"value": "Real GDP"}),
        "cpi_df": pd.DataFrame(raw_data["cpi"]["data"]).set_index("date").astype(float).rename(columns={"value": "CPI"}),
        "inflation_df": pd.DataFrame(raw_data["inflation"]["data"]).set_index("date").astype(float).rename(columns={"value": "Inflation Rate"}),
        "federal_funds_rate_df": pd.DataFrame(raw_data["federal_funds_rate"]["data"]).set_index("date").astype(float).rename(columns={"value": "Federal Funds Rate"}),
        "retail_sales_df": pd.DataFrame(raw_data["retail_sales"]["data"]).set_index("date").astype(float).rename(columns={"value": "Retail Sales"}),
        "unemployment_rate_df": pd.DataFrame(raw_data["unemployment"]["data"]).set_index("date").astype(float).rename(columns={"value": "Unemployment Rate"}),
    }
    for df_name, df_micro in micro_dfs.items():
        df_micro.index = pd.DatetimeIndex(df_micro.index)
    return micro_dfs


def get_technical_indicator_df_data(indicator_raw_data):
    technical_indicator_dfs = {}

    technical_indicator_dfs["SMA"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["SMA"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["SMA"][f"Technical Analysis: SMA"].keys()),
            "SMA": get_technical_analysis_values(
                tech_analysis_dict=indicator_raw_data["SMA"]["Technical Analysis: SMA"],
                tech_analysis_name="SMA"),
        }).set_index("date")
    }

    technical_indicator_dfs["EMA"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["EMA"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["EMA"][f"Technical Analysis: EMA"].keys()),
            "EMA": get_technical_analysis_values(
                tech_analysis_dict=indicator_raw_data["EMA"]["Technical Analysis: EMA"],
                tech_analysis_name="EMA"),
        }).set_index("date")
    }

    technical_indicator_dfs["RSI"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["RSI"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["RSI"][f"Technical Analysis: RSI"].keys()),
            "RSI": get_technical_analysis_values(
                tech_analysis_dict=indicator_raw_data["RSI"]["Technical Analysis: RSI"],
                tech_analysis_name="RSI"),
        }).set_index("date")
    }

    technical_indicator_dfs["MACD"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["MACD"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["MACD"][f"Technical Analysis: MACD"].keys()),
            "MACD": get_technical_analysis_values(
                tech_analysis_dict=indicator_raw_data["MACD"]["Technical Analysis: MACD"],
                tech_analysis_name="MACD"),
        }).set_index("date")
    }

    bbands_values = get_bbands_technical_analysis_values(tech_analysis_dict=indicator_raw_data["BBANDS"]["Technical Analysis: BBANDS"])

    technical_indicator_dfs["BBANDS"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["BBANDS"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["BBANDS"][f"Technical Analysis: BBANDS"].keys()),
            "lowerBound": bbands_values["lowerBound"],
            "middleBound": bbands_values["middleBound"],
            "upperBound": bbands_values["upperBound"],
        }).set_index("date")
    }

    technical_indicator_dfs["ADX"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["ADX"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["ADX"][f"Technical Analysis: ADX"].keys()),
            "ADX": get_technical_analysis_values(
                tech_analysis_dict=indicator_raw_data["ADX"]["Technical Analysis: ADX"],
                tech_analysis_name="ADX"),
        }).set_index("date")
    }

    technical_indicator_dfs["AD"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["AD"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["AD"][f"Technical Analysis: Chaikin A/D"].keys()),
            "AD": get_technical_analysis_values(
                tech_analysis_dict=indicator_raw_data["AD"]["Technical Analysis: Chaikin A/D"],
                tech_analysis_name="Chaikin A/D"),
        }).set_index("date")
    }

    technical_indicator_dfs["OBV"] = {
        "Meta Data": pd.DataFrame([indicator_raw_data["OBV"]["Meta Data"]]),
        "Technical Analysis Data": pd.DataFrame({
            "date": pd.DatetimeIndex(indicator_raw_data["OBV"][f"Technical Analysis: OBV"].keys()),
            "OBV": get_technical_analysis_values(
                tech_analysis_dict=indicator_raw_data["OBV"]["Technical Analysis: OBV"],
                tech_analysis_name="OBV"),
        }).set_index("date")
    }

    return technical_indicator_dfs

