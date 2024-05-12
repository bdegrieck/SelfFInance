from BackEnd.Data.api import get_earnings_calender_endpoints, get_raw_api_csv_dfs
from BackEnd.Data.calender import EarningsCalender


class TestCalenderEarnings:

    def test_calenders(self):

        ticker = "AAPL"
        earnings_calender = EarningsCalender(ticker=ticker)
