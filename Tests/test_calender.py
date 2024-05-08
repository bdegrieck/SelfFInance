from BackEnd.Data.api import get_earnings_calender_endpoints, get_raw_api_csv_dfs


class TestCalenderEarnings:

    def test_calenders(self):

        ticker = "AAPL"
        endpoints = get_earnings_calender_endpoints(ticker=ticker)
        calender_dfs = get_raw_api_csv_dfs(endpoints=endpoints)
        print(calender_dfs)
