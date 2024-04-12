import requests

from BackEnd import constants
from BackEnd.error import SameTickers, EnterTickerInstead, TickerDoesNotExist, EmptyInput


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


# checks if user input field are blank
def check_for_blank_ticker_input(user_input_tickers: list):
    for ticker_number in range(len(user_input_tickers)):
        if user_input_tickers[ticker_number] is None or user_input_tickers[ticker_number] == "":
            raise EmptyInput(f"Ticker: {ticker_number + 1} is empty")


class UserInput:
    def __init__(self, raw_user_input):
        self.raw_tickers_input = format_ticker_input(user_input_tickers=raw_user_input["Ticker Input"])
        self.micro_input = raw_user_input["Microeconomic Input"]
        self.news_input = raw_user_input["News Input"]
        self.endpoints_input = raw_user_input["Endpoints Input"]


# check tickers and reformat tickers
def format_ticker_input(user_input_tickers: list) -> list:
    check_for_blank_ticker_input(user_input_tickers=user_input_tickers)
    for ticker_number in range(len(user_input_tickers)):
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={user_input_tickers[ticker_number]}&apikey={constants.API_KEY}'
        ticker_list = requests.get(url).json()

        name_input = check_extraneous_tickers(input_name=user_input_tickers[ticker_number].lower().strip())
        if name_input:
            user_input_tickers[ticker_number] = name_input
            continue

        if len(ticker_list["bestMatches"]) == 0:
            raise TickerDoesNotExist(f'Your input "{user_input_tickers[ticker_number]}" does not exist')

        # filter out invalid tickers
        better_matches = []
        for match in range(0, len(ticker_list["bestMatches"])):
            if "." not in ticker_list["bestMatches"][match]["1. symbol"] and "-" not in \
                    ticker_list["bestMatches"][match]["1. symbol"]:
                better_matches.append(ticker_list["bestMatches"][match]["1. symbol"])

        if len(better_matches) == 0:
            raise EnterTickerInstead(f'Please enter ticker instead of "{user_input_tickers[ticker_number]}"')
        else:
            user_input_tickers[ticker_number] = better_matches[0]

    # checks if tickers are the same for comparison
    if len(user_input_tickers) > 1 and user_input_tickers[0] == user_input_tickers[1]:
        raise SameTickers("Please input two different tickers")
    return user_input_tickers
