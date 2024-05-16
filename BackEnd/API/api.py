import csv

import requests
from pydantic import BaseModel, HttpUrl

from BackEnd import constants
from BackEnd.API.calenderrawdata import CompanyEarningsCalendar, UpcomingEarningsCalendar, EarningsCalendar
from BackEnd.API.companyrawdata import TimeSeriesData, CompanyEPS, CompanyRawData, CompanyIncomeStatement, \
    CompanyCashFlow, CompanyOverview
from BackEnd.API.microrawdata import RealGDP, CPI, InflationRates, InterestRates, RetailSales, UnemploymentRates, MicroRawData
from BackEnd.API.technicalindicatorrawdata import SMA, EMA, BBANDS, RSI, AD, ADX, OBV, MACD, TechnicalIndicatorsRawData
from BackEnd.Data.dataclean import check_raw_data


# get raw data endpoints are passed in
def get_raw_api_data(endpoints) -> dict:
    raw_data = {}
    for data_description, endpoint_url in endpoints.dict().items():
        raw_data[data_description] = requests.get(url=endpoint_url).json()
    check_raw_data(ticker_raw_data=raw_data)
    return raw_data


# decodes only csv
def get_raw_api_csv_dfs(endpoints):
    raw_data = {}
    for csv_type, csv_endpoint in endpoints.dict().items():
        with requests.Session() as s:
            download = s.get(csv_endpoint)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            raw_data[csv_type] = list(cr)
    return raw_data


class CompanyEndpoints(BaseModel):
    times_series_data: HttpUrl
    overview: HttpUrl
    income_statement: HttpUrl
    balance_sheet: HttpUrl
    cash_flow: HttpUrl
    earnings: HttpUrl


class MicroEndpoints(BaseModel):
    real_gdp: HttpUrl
    cpi: HttpUrl
    inflation: HttpUrl
    federal_funds_rate: HttpUrl
    retail_sales: HttpUrl
    unemployment: HttpUrl


class CalenderEndpoints(BaseModel):
    upcoming_earnings_calender: HttpUrl
    company_earnings_calender: HttpUrl


class TechnicalIndicatorEndpoints(BaseModel):
    SMA: HttpUrl
    EMA: HttpUrl
    RSI: HttpUrl
    MACD: HttpUrl
    BBANDS: HttpUrl
    ADX: HttpUrl
    AD: HttpUrl
    OBV: HttpUrl


# format raw data to specific data returns a dictionary of dfs
def get_company_raw_data(company_raw_data: dict) -> CompanyRawData:

    company_prices = [TimeSeriesData(
        date=date,
        high=data["2. high"],
        low=data["3. low"],
        close=data["5. adjusted close"],
        volume=data["6. volume"],
    ) for date, data in company_raw_data["times_series_data"]["Time Series (Daily)"].items()]

    company_overview = CompanyOverview(
        ticker_symbol=company_raw_data["overview"]["Symbol"],
        company_description=company_raw_data["overview"]["Description"],
        market_cap=company_raw_data["overview"]["MarketCapitalization"],
        year_price_high=company_raw_data["overview"]["52WeekHigh"],
        year_price_low=company_raw_data["overview"]["52WeekLow"]
    )

    company_eps = [CompanyEPS(
        estimated_eps=data["estimatedEPS"],
        reported_eps=data["reportedEPS"],
        surprise_percentage=data["surprisePercentage"],
        reported_date=data["reportedDate"]
    ) for data in company_raw_data["earnings"]["quarterlyEarnings"]]

    company_cashflow = [CompanyCashFlow(
        quarter_date=data["fiscalDateEnding"],
        cashflow_from_investment=data["cashflowFromInvestment"],
        cashflow_from_financing=data["cashflowFromFinancing"],
        cashflow_from_operations=data["operatingCashflow"],
    ) for data in company_raw_data["cash_flow"]["quarterlyReports"]]

    company_income_statement = [CompanyIncomeStatement(
        quarter_date=data["fiscalDateEnding"],
        profit=data["netIncome"],
        revenue=data["totalRevenue"]
    ) for data in company_raw_data["income_statement"]["quarterlyReports"]]

    company_data = CompanyRawData(
        company_prices=company_prices,
        company_overview=company_overview,
        company_eps=company_eps,
        company_income_statement=company_income_statement,
        company_cashflow=company_cashflow
    )

    return company_data


def get_micro_raw_data(raw_data: dict) -> MicroRawData:

    real_gdp = [RealGDP(date=data["date"], real_gdp=data["value"]) for data in raw_data["real_gdp"]["data"]]
    cpi = [CPI(date=data["date"], cpi=data["value"]) for data in raw_data["cpi"]["data"]]
    inflation_rates = [InflationRates(date=data["date"], inflation_rate=data["value"]) for data in raw_data["inflation"]["data"]]
    interest_rates = [InterestRates(date=data["date"], interest_rate=data["value"]) for data in raw_data["federal_funds_rate"]["data"]]
    retail_sales = [RetailSales(date=data["date"], retail_sale=data["value"]) for data in raw_data["retail_sales"]["data"]]
    unemployment_rates = [UnemploymentRates(date=data["date"], unemployment_rate=data["value"]) for data in raw_data["unemployment"]["data"]]

    micro_raw_data = MicroRawData(
        real_gdp=real_gdp,
        cpi=cpi,
        inflation_rates=inflation_rates,
        interest_rates=interest_rates,
        retail_sales=retail_sales,
        unemployment_rates=unemployment_rates
    )

    return micro_raw_data


def get_technical_indicator_raw_data(indicator_raw_data) -> TechnicalIndicatorsRawData:

    sma = [SMA(
        date=data,
        sma=indicator_raw_data["SMA"]["Technical Analysis: SMA"][data]["SMA"]
    ) for data in indicator_raw_data["SMA"]["Technical Analysis: SMA"]]

    ema = [EMA(
        date=data,
        ema=indicator_raw_data["EMA"]["Technical Analysis: EMA"][data]["EMA"]
    ) for data in indicator_raw_data["EMA"]["Technical Analysis: EMA"]]

    rsi = [RSI(
        date=data,
        rsi=indicator_raw_data["RSI"]["Technical Analysis: RSI"][data]["RSI"]
    ) for data in indicator_raw_data["RSI"]["Technical Analysis: RSI"]]

    macd = [MACD(
        date=data,
        macd=indicator_raw_data["MACD"]["Technical Analysis: MACD"][data]["MACD"]
    ) for data in indicator_raw_data["MACD"]["Technical Analysis: MACD"]]

    bbands = [BBANDS(
            date=data,
            lower_band=indicator_raw_data["BBANDS"]["Technical Analysis: BBANDS"][data]["Real Lower Band"],
            middle_band=indicator_raw_data["BBANDS"]["Technical Analysis: BBANDS"][data]["Real Middle Band"],
            upper_band=indicator_raw_data["BBANDS"]["Technical Analysis: BBANDS"][data]["Real Upper Band"],
        )
        for data in indicator_raw_data["BBANDS"]["Technical Analysis: BBANDS"]
    ]

    adx = [ADX(
        date=data,
        adx=indicator_raw_data["ADX"]["Technical Analysis: ADX"][data]["ADX"]
    ) for data in indicator_raw_data["ADX"]["Technical Analysis: ADX"]]

    ad = [AD(
        date=data,
        ad=indicator_raw_data["AD"]["Technical Analysis: Chaikin A/D"][data]['Chaikin A/D']
    ) for data in indicator_raw_data["AD"]["Technical Analysis: Chaikin A/D"]]

    obv = [OBV(
        date=data,
        obv=indicator_raw_data["OBV"]["Technical Analysis: OBV"][data]["OBV"]
    ) for data in indicator_raw_data["OBV"]["Technical Analysis: OBV"]]

    technical_indicator_raw_data = TechnicalIndicatorsRawData(
        sma=sma,
        ema=ema,
        rsi=rsi,
        macd=macd,
        bbands=bbands,
        adx=adx,
        ad=ad,
        obv=obv
    )

    return technical_indicator_raw_data


def get_calender_raw_data(raw_data: dict):

    company_earnings_calendar = [CompanyEarningsCalendar(
        symbol=data[0],
        report_date=data[2],
        quarter_date=data[3],
        eps_estimate=data[4]
    ) for data in raw_data["company_earnings_calender"][1:]]

    upcoming_earnings_calendar = [UpcomingEarningsCalendar(
        symbol=data[0],
        company_name=data[1],
        report_date=data[2],
        quarter_date=data[3],
        eps_estimate=data[4],
        currency=data[5]
    ) for data in raw_data["upcoming_earnings_calender"][1:]]

    calender_raw_data = EarningsCalendar(
        company_earnings_calendar=company_earnings_calendar,
        upcoming_earnings_calendar=upcoming_earnings_calendar
    )

    return calender_raw_data


# format company endpoints
def get_company_endpoints(ticker: str) -> CompanyEndpoints:
    endpoints = CompanyEndpoints(
        times_series_data=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={constants.API_KEY}&outputsize=full",
        overview=f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={constants.API_KEY}",
        income_statement=f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={constants.API_KEY}",
        balance_sheet=f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={constants.API_KEY}",
        cash_flow=f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={constants.API_KEY}",
        earnings=f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={constants.API_KEY}",
    )

    return endpoints


def get_micro_endpoints() -> MicroEndpoints:
    endpoints = MicroEndpoints(
        real_gdp=f"https://www.alphavantage.co/query?function=REAL_GDP&symbol=AAPL&apikey={constants.API_KEY}",
        cpi=f"https://www.alphavantage.co/query?function=CPI&symbol=AAPL&apikey={constants.API_KEY}",
        inflation=f"https://www.alphavantage.co/query?function=INFLATION&symbol=AAPL&apikey={constants.API_KEY}",
        federal_funds_rate=f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&symbol=AAPL&apikey={constants.API_KEY}",
        retail_sales=f"https://www.alphavantage.co/query?function=RETAIL_SALES&symbol=AAPL&apikey={constants.API_KEY}",
        unemployment=f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&symbol=AAPL&apikey={constants.API_KEY}"
    )

    return endpoints


def get_earnings_calender_endpoints(ticker: str) -> CalenderEndpoints:
    endpoints = CalenderEndpoints(
        upcoming_earnings_calender=f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={constants.API_KEY}",
        company_earnings_calender=f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={ticker}&horizon=12month&apikey={constants.API_KEY}"
    )

    return endpoints


def get_technical_indicator_endpoints(ticker: str):
    endpoints = TechnicalIndicatorEndpoints(
        # (Simple Moving Average) Averages the price over a specific period to identify trend directions
        SMA=f'https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

        # (Exponential Moving Average) Similar to SMA but gives more weight to recent prices, making it more responsive to recent price changes
        EMA=f'https://www.alphavantage.co/query?function=EMA&symbol={ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

        # (Relative Strength Index) A momentum indicator that measures the speed and change of price movements to identify overbought or oversold conditions
        RSI=f'https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval=weekly&time_period=10&series_type=open&apikey={constants.API_KEY}',

        # (Moving Average Convergence Divergence): Measures the relationship between two moving averages to identify trends and momentum shifts
        MACD=f'https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval=daily&series_type=open&apikey={constants.API_KEY}',

        # Bollinger Bands used to identify periods of high or low volatility based on moving averages
        BBANDS=f'https://www.alphavantage.co/query?function=BBANDS&symbol={ticker}&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey={constants.API_KEY}',

        # (Average Directional Index): Measures the strength of a trend
        ADX=f'https://www.alphavantage.co/query?function=ADX&symbol={ticker}&interval=daily&time_period=10&apikey={constants.API_KEY}',

        # (Accumulation/Distribution) Useful for determining the strength of trends by showing if price movements are supported by strong buying or selling pressure
        AD=f'https://www.alphavantage.co/query?function=AD&symbol={ticker}&interval=daily&apikey={constants.API_KEY}',

        # (On-Balance Volume)  Often used as a leading indicator, suggesting potential trend reversals before price action confirms them
        OBV=f'https://www.alphavantage.co/query?function=OBV&symbol={ticker}&interval=weekly&apikey={constants.API_KEY}'
    )

    return endpoints
