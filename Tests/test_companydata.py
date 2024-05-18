import pytest

from BackEnd.Data.companydata import CompanyData
from BackEnd.error import TickerDoesNotExist
from BackEnd.user import UserInput


class TestCompanyData:

    def test_ticker_inputs(self):
        # test with gibberish
        with pytest.raises(TickerDoesNotExist):
            user_input = "sfafdsafasfds"
            input = UserInput(tickers=[user_input])


        # test with a company that just went public on 5/13/24
        user_input = "USOY"
        input = UserInput(tickers=["USOY"])
        data = CompanyData(ticker=input.tickers[0])
        print("hi")
