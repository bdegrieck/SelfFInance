from pydantic import BaseModel, validator
from typing import List, Optional


class BaseEarningsCalendar(BaseModel):
    eps_estimate: Optional[float]  # Declare this here if it's common to all subclasses

    # Shared validator for handling 'eps_estimate'
    @validator('eps_estimate', pre=True)
    def handle_na_eps(cls, value):
        if isinstance(value, str) and (value == "" or value == "None"):
            return None
        return value


class CompanyEarningsCalendar(BaseEarningsCalendar):
    symbol: str
    report_date: str
    quarter_date: str


class UpcomingEarningsCalendar(BaseEarningsCalendar):
    symbol: str
    company_name: str
    report_date: str
    quarter_date: str
    currency: str


class EarningsCalendar(BaseModel):
    company_earnings_calendar: List[CompanyEarningsCalendar]
    upcoming_earnings_calendar: List[UpcomingEarningsCalendar]
