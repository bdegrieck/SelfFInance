import datetime
from typing import List, Optional
import datetime as dt
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
    report_date: dt.datetime
    quarter_date: dt.datetime
    currency: Optional[str]

    # checks if currency is USD instead of European stocks
    @validator("currency", pre=True)
    def handle_currency_values(cls, value):
        if isinstance(value, str) and value != "USD":
            return None
        return value

    # checks if valid ticker that is in the NYSE
    @validator("symbol", pre=True)
    def handle_invalid_tickers(cls, ticker):
        if isinstance(ticker, str) and len(ticker) > 4:
            return None
        return ticker

    # filters calenders that will
    @validator("report_date", pre=True)
    def handle_report_dates_within_range(cls, date):
        todays_date = dt.datetime.today()
        next_date = todays_date + dt.timedelta(days=2)

        # Convert the dates to strings in the desired format
        todays_date_str = todays_date.strftime('%Y-%m-%d')
        next_date_str = next_date.strftime('%Y-%m-%d')

        if todays_date <= date <= next_date:
            return date
        return None


class EarningsCalendar(BaseModel):
    company_earnings_calendar: List[CompanyEarningsCalendar]
    upcoming_earnings_calendar: List[UpcomingEarningsCalendar]
