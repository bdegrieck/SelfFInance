import requests

from BackEnd import constants


# formats user inputted ticker to most relevant search done by api
def get_formatted_ticker(ticker: str) -> str:
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={constants.API_KEY}'
    ticker = requests.get(url).json()
    return ticker["bestMatches"][0]["1. symbol"]


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

def check_same_tickers(ticker1: str, ticker2: str):
    if ticker1 == ticker2:
        return f"Please input two different tickers"
