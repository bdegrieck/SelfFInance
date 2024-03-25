import requests

from BackEnd import constants


def check_extraneous_tickers(input_name: str):
    extraneous_tickers = {
        "microsoft": "MSFT",
        "apple": "AAPL",
        "tesla": "TSLA",
        "target": "TGT"
    }
    for name, ticker in extraneous_tickers.items():
        if input_name == name:
            return ticker


# formats user inputted ticker to most relevant search done by api
def get_formatted_ticker(ticker: str) -> str:
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={constants.API_KEY}'
    ticker_list = requests.get(url).json()
    name_input = check_extraneous_tickers(input_name=ticker.lower().strip())
    if name_input:
        return name_input
    elif len(ticker_list["bestMatches"][0]["1. symbol"]) > 4:
        return f'Enter ticker instead of "{ticker}"'
    else:
        return ticker_list["bestMatches"][0]["1. symbol"]


# checks user input for a valid ticker that api can detect
def valid_ticker_input(ticker: str) -> str:
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={constants.API_KEY}'
    best_matches = requests.get(url).json()
    if len(best_matches["bestMatches"]) == 0:
        return "Your inputted Ticker does not exist"


# informs user what field was left blank
def validate_user_input(user_input: dict) -> str:
    for input_type, input_value in user_input.items():
        if not input_value:
            return f"{input_type}: is empty"


# informs user to select at least one endpoint
def validate_endpoints(user_input: dict) -> str:
    if not any(user_input.values()):
        return f'Please select at least one options:{list(user_input.keys())}'


# checks if two tickers are the same for comparison
def check_same_tickers(ticker1: str, ticker2: str):
    if ticker1 == ticker2:
        return "Please input two different tickers"
