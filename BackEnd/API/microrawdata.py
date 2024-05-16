import datetime
from typing import List

from pydantic import BaseModel


class RealGDP(BaseModel):
    date: datetime.datetime
    real_gdp: float


class CPI(BaseModel):
    date: datetime.datetime
    cpi: float


class InflationRates(BaseModel):
    date: datetime.datetime
    inflation_rate: float


class RetailSales(BaseModel):
    date: datetime.datetime
    retail_sale: float


class InterestRates(BaseModel):
    date: datetime.datetime
    interest_rate: float


class UnemploymentRates(BaseModel):
    date: datetime.datetime
    unemployment_rate: float


class MicroRawData(BaseModel):
    real_gdp: List[RealGDP]
    cpi: List[CPI]
    inflation_rates: List[InflationRates]
    retail_sales: List[RetailSales]
    interest_rates: List[InterestRates]
    unemployment_rates: List[UnemploymentRates]