import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


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
    report_date: datetime.datetime
    quarter_date: datetime.datetime


class UpcomingEarningsCalendar(BaseEarningsCalendar):
    symbol: str
    company_name: str
    report_date: datetime.datetime
    quarter_date: datetime.datetime
    currency: str


class EarningsCalendar(BaseModel):
    company_earnings_calendar: List[CompanyEarningsCalendar]
    upcoming_earnings_calendar: List[UpcomingEarningsCalendar]
