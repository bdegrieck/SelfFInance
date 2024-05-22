from BackEnd.formatinput import UserInput

from BackEnd.Data.tickercomparison import TickerComparison
from BackEnd.user import User


class TestTickerComparison:

    def test_ticker_comparison(self):
        input_raw = UserInput({"Ticker Input": ["apple", "microsoft"]})
        input = User(input_raw)
        comparison = TickerComparison(input.company_data[0], input.company_data[1])