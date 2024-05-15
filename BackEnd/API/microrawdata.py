import datetime
from typing import List

from pydantic import BaseModel


class RealGDP(BaseModel):
    date: datetime.datetime
    real_gdp: float


class CPI(BaseModel):
    date: datetime.datetime
    cpi: float


class Inflation(BaseModel):
    date: datetime.datetime
    inflation_rate: float


class RetailSales(BaseModel):
    date: datetime.datetime
    retail_sales: float


class InterestRates(BaseModel):
    date: datetime.datetime
    interest_rate: float


class UnemploymentRate(BaseModel):
    date: datetime.datetime
    unemployment_rate: float


class MicroRawData(BaseModel):
    real_gdp: List[RealGDP]
    cpi: List[CPI]
    inflation: List[Inflation]
    retail_sales: List[RetailSales]
    interest_rate: List[InterestRates]
    unemployment_rate: List[UnemploymentRate]