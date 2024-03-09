from BackEnd.microData import MicroData
from BackEnd.companyData import CompanyData
from BackEnd.compare import Compare


class User:
    api_key = "CRU63X7J4COJ46F2"
    user_input_ticker = "AAPL"
    second_input_ticker = "MSFT"

    user_main_ticker = CompanyData(ticker=user_input_ticker, api_key=api_key)
    user_second_ticker = CompanyData(ticker=second_input_ticker, api_key=api_key)
    #user_micro = MicroData(ticker=user_input_ticker, api_key=api_key)

    Compare(main_ticker_data=user_main_ticker, second_ticker_data=user_second_ticker)



