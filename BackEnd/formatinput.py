import requests
from flask import flash, redirect, url_for

from BackEnd import constants


# tickers that the api cannot understand when inputting full company name instead of ticker
def check_extraneous_tickers(input_name: str):
    extraneous_tickers = {
        "apple": "AAPL",
        "target": "TGT",
        "google": "GOOGL",
        "disney": "DIS",
        "at&t": "T",
        "visa": "V",
        "berkshire hathaway": "BRK",
        "eli lily & co": "LLY",
        "eli lily and co": "LLY",
        "eli lily": "LLY",
        "chase": "JPM",
        "jpmorgan": "JPM",
        "johnson & johnson": "JNJ",
        "johnson and johnson": "JNJ",
        "coca cola": "KO",
        "mcdonalds": "MCD",
    }
    if input_name in extraneous_tickers.keys():
        return extraneous_tickers[input_name]


class FormatInput:

    def __init__(self, user_input: dict):
        self.check_for_blank_input(user_input=user_input)
        self.user_input = self.check_ticker_input(user_input=user_input["Ticker Input"])

    def check_for_blank_input(self, user_input: dict):
        for input_type, input_value in user_input.items():
            if input_type is dict:
                if not any(user_input.values()):
                    flash( f'Please select at least one options:{list(user_input.keys())}')
                    return redirect(url_for("views.home"))
            else:
                if not input_value:
                    flash(f"{input_type}: is empty")
                    return redirect(url_for("views.home"))

    def check_ticker_input(self, user_input: list):



    # formats user inputted ticker to most relevant search done by api
    def get_formatted_ticker(self, ticker: str) -> str:
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={constants.API_KEY}'
        ticker_list = requests.get(url).json()

        name_input = check_extraneous_tickers(input_name=ticker.lower().strip())
        if name_input:
            return name_input

        if len(ticker_list["bestMatches"]) == 0:
            return f'Your input "{ticker}" does not exist'

        # filter out invalid tickers
        better_matches = []
        for match in range(0, len(ticker_list["bestMatches"])):
            if "." not in ticker_list["bestMatches"][match]["1. symbol"] and "-" not in ticker_list["bestMatches"][match]["1. symbol"]:
                better_matches.append(ticker_list["bestMatches"][match]["1. symbol"])

        if len(better_matches) == 0:
            return f'Please enter ticker instead of "{ticker}"'
        else:
            return better_matches[0]


    # checks user input for a valid ticker that api can detect
    def valid_ticker_input(ticker: str) -> str:
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={constants.API_KEY}'
        best_matches = requests.get(url).json()
        check_extraneous = check_extraneous_tickers(input_name=ticker)
        if len(best_matches["bestMatches"]) == 0 and check_extraneous is None:
            return "Your inputted Ticker does not exist"


    # informs user what field was left blank
    def validate_user_input(user_input: dict) -> str:
        for input_type, input_value in user_input.items():
            if not input_value:
                return f"{input_type}: is empty"
        if not any(user_input["Endpoints"].values()):
            return f'Please select at least one options:{list(user_input.keys())}'


    # informs user to select at least one endpoint
    def validate_endpoints(user_input: dict) -> str:
        if not any(user_input.values()):
            return f'Please select at least one options:{list(user_input.keys())}'


    # checks if two tickers are the same for comparison
    def check_same_tickers(ticker1: str, ticker2: str):
        if ticker1 == ticker2:
            return "Please input two different tickers"


    def check_raw_data(ticker_raw_data: dict) -> str:
        for raw_data_dict in ticker_raw_data:
            if not raw_data_dict:
                return "Inputted ticker does not have enough data to display"
