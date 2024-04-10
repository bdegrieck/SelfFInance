from BackEnd.companyData import CompanyData
from BackEnd.tickercomparison import TickerComparison
from BackEnd.error import valid_ticker_input, get_formatted_ticker, validate_user_input
from BackEnd.news import News


class TestWholeTicker:
    # purpose of this test is to test random instances for debugging not part of phase 4
    def test_ticker(self):
        user_input = {
            "Ticker1": "nvdy",
            "Ticker2": "reddit",
        }
        assert validate_user_input(user_input=user_input) is None

        ticker1 = get_formatted_ticker(ticker=user_input["Ticker1"])
        ticker2 = get_formatted_ticker(ticker=user_input["Ticker2"])

        comparison = TickerComparison(ticker1, ticker2)
        print("hi")


