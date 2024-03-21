import requests

from BackEnd import constants
from BackEnd.data import get_raw_api_data
from BackEnd.microData import MicroData
from BackEnd.companyData import CompanyData
from BackEnd.compare import Compare
from BackEnd.news import News


class User:

    user_input_ticker = "AAPL"
    api_key = constants.API_KEY

    micro_data = MicroData()

    #user_main_ticker = CompanyData(ticker=user_input_ticker)
    second_ticker = CompanyData(ticker="IBM")
    #comparison_data = Compare(user_main_ticker, second_ticker)
    print("hi")
