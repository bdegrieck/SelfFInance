from pydantic import BaseModel
from typing import List


class RealGDP(BaseModel):
    date: str
    real_gdp: float


class CPI(BaseModel):
    date: str
    cpi: float


class Inflation(BaseModel):
    date: str
    inflation_rate: float


class RetailSales(BaseModel):
    date: str
    retail_sales: float


class InterestRates(BaseModel):
    date: str
    interest_rate: float


class UnemploymentRate(BaseModel):
    date: str
    unemployment_rate: float


class MicroRawData(BaseModel):
    real_gdp: List[RealGDP]
    cpi: List[CPI]
    inflation: List[Inflation]
    retail_sales: List[RetailSales]
    interest_rate: List[InterestRates]
    unemployment_rate: List[UnemploymentRate]