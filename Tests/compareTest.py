from BackEnd.errors import get_formatted_ticker, check_same_tickers, valid_ticker_input


class TestCompare:

    # check if tickers are the same then display error message
    def test_compare_tickers(self):
        ticker1 = "AAPL"
        ticker2 = "aapl"
        ticker1 = get_formatted_ticker(ticker=ticker1)
        ticker2 = get_formatted_ticker(ticker=ticker2)
        check = check_same_tickers(ticker1, ticker2)

    def test_formatted_ticker(self):
        ticker = "safhlashglashglah"
        ticker_valid_message = valid_ticker_input(ticker=ticker)
        ticker_fixed = get_formatted_ticker(ticker=ticker)
