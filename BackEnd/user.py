import requests
from BackEnd.data import get_raw_api_data
from BackEnd.microData import MicroData
from BackEnd.companyData import CompanyData
from BackEnd.compare import Compare


def get_ticker(ticker: str, api_key:str) -> str:
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={api_key}'
    ticker = requests.get(url).json()["bestMatches"][0]["1. symbol"]
    return ticker


class User:
    def __init__(self, intput_ticker: str):
        self.api_key = "CRU63X7J4COJ46F2"
        self.input_ticker = get_ticker(ticker=intput_ticker, api_key=self.api_key)
        self.main_ticker_data = CompanyData(ticker=self.input_ticker, api_key=self.api_key)
        #self.micro_data = MicroData(ticker=self.input_ticker, api_key=self.api_key)

    user_input_ticker = "AAPL"
    api_key = "CRU63X7J4COJ46F2"

    micro_data = MicroData(user_input_ticker, api_key)

    user_main_ticker = CompanyData(ticker=user_input_ticker, api_key=api_key)
    print("hi")
    #user_second_ticker = CompanyData(ticker=second_input_ticker, api_key=api_key)
    #user_micro = MicroData(ticker=user_input_ticker, api_key=api_key)

    #Compare(main_ticker_data=user_main_ticker, second_ticker_data=user_second_ticker)



