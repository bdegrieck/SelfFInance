from BackEnd.errors import get_formatted_ticker, valid_ticker_input, check_same_tickers


class TestErrors:

    def test_user_valid_inputs(self):

        # test company full name
        ticker = "microsoft"

        assert valid_ticker_input(ticker=ticker) is None
        assert get_formatted_ticker(ticker=ticker) == "MSFT"

        # test space after input
        ticker = "apple "

        assert valid_ticker_input(ticker=ticker) is None
        assert get_formatted_ticker(ticker=ticker) == "AAPL"

        # test lower case ticker
        ticker = "tsla"

        assert valid_ticker_input(ticker=ticker) is None
        assert get_formatted_ticker(ticker=ticker) == "TSLA"

        # test upper case ticker
        ticker = "NVDA"

        assert valid_ticker_input(ticker=ticker) is None
        assert get_formatted_ticker(ticker=ticker) == "NVDA"

        # test ETF
        ticker = "QQQ"

        assert valid_ticker_input(ticker=ticker) is None
        assert get_formatted_ticker(ticker=ticker) == "QQQ"

        # test company that just went public reddit
        ticker = "reddit"
        assert valid_ticker_input(ticker=ticker) is None
        assert get_formatted_ticker(ticker=ticker) == "RDDT"

    def test_check_same_tickers_input(self):
        # test if user enters two of the same tickers which informs user to re enter a new ticker
        ticker1 = "AAPL"
        ticker2 = "AAPL"

        assert valid_ticker_input(ticker=ticker1) is None
        assert valid_ticker_input(ticker=ticker2) is None

        ticker1 = get_formatted_ticker(ticker1)
        ticker2 = get_formatted_ticker(ticker2)

        assert check_same_tickers(ticker1=ticker1, ticker2=ticker2) == "Please input two different tickers"

        # test if user enters two of the same tickers but with company name and ticker symbol
        ticker1 = "delta air lines"
        ticker2 = "DAL"

        assert valid_ticker_input(ticker=ticker1) is None
        assert valid_ticker_input(ticker=ticker2) is None

        ticker1 = get_formatted_ticker(ticker1)
        ticker2 = get_formatted_ticker(ticker2)

        assert check_same_tickers(ticker1=ticker1, ticker2=ticker2) == "Please input two different tickers"

    def test_invalid_tickers(self):
        # test invalid ticker
        ticker = "sfhasdklfhalksgh"
        assert valid_ticker_input(ticker=ticker) == "Your inputted Ticker does not exist"

        # test company that went private (twitter went private before being bought by Elon)
        ticker = "TWTR"
        assert valid_ticker_input(ticker=ticker) == "Your inputted Ticker does not exist"

        # test non american  ticker which is invalid
        ticker = "MMIG.F"
        assert valid_ticker_input(ticker=ticker) == "Your inputted Ticker does not exist"
