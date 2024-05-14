from typing import Optional, List

from pydantic import BaseModel, validator


class TimeSeriesData(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float


class CompanyOverview(BaseModel):
    ticker_symbol: str
    company_description: str
    market_cap: float
    year_price_high: float
    year_price_low: float


class CompanyEPS(BaseModel):
    estimated_eps: Optional[float]
    reported_eps: Optional[float]
    surprise_percentage: Optional[float]
    reported_date: str

    @validator("estimated_eps", "reported_eps", "surprise_percentage", pre=True, allow_reuse=True)
    def handle_none_values(cls, value):
        if isinstance(value, str) and value == 'None':
            return None
        return value


class CompanyCashFlow(BaseModel):
    quarter_date: str
    cashflow_from_investment: Optional[float]
    cashflow_from_financing: Optional[float]
    cashflow_from_operations: Optional[float]

    @validator("cashflow_from_investment", "cashflow_from_financing", "cashflow_from_operations", pre=True, allow_reuse=True)
    def handle_none_values(cls, value):
        if isinstance(value, str) and value == 'None':
            return None
        return value


class CompanyIncomeStatement(BaseModel):
    quarter_date: str
    profit: Optional[float]
    revenue: Optional[float]

    @validator("profit", "revenue", pre=True, allow_reuse=True)
    def handle_none_values(cls, value):
        if isinstance(value, str) and value == 'None':
            return None
        return value


class CompanyRawData(BaseModel):
    company_prices: List[TimeSeriesData]
    company_overview: CompanyOverview
    company_eps: List[CompanyEPS]
    company_cashflow: List[CompanyCashFlow]
    company_income_statement: List[CompanyIncomeStatement]
