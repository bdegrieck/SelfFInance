import requests

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

class Error:

    def __init__(self, user_input: dict):
        self.tickers = user_input["Ticker Input"]
        self.error_message = None
        self.check_blank_input(user_input=user_input)
        self.formatted_tickers = self.format_tickers_input(tickers_input=self.tickers)

    def get_error_message(self, error_msg: str):


    # checks for blank input
    def check_blank_input(self, user_input: dict):
        for input_type, input_value in user_input.items():
            if input_type is dict:
                if not any(user_input.values()):
                    return f'Please select at least one options:{list(user_input.keys())}'
            else:
                if not input_value:
                    return f"{input_type}: is empty"

    def format_tickers_input(self, tickers_input: dict):
        for ticker_type, ticker_value in tickers_input.items():
            url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker_type}&apikey={constants.API_KEY}'
            best_ticker_matches = requests.get(url).json()
            check_extraneous = check_extraneous_tickers(input_name=ticker_type)
            if len(best_ticker_matches["bestMatches"]) == 0 and check_extraneous is None:
                self.error_message = "Your inputted Ticker does not exist"

            name_input = check_extraneous_tickers(input_name=ticker_value.lower().strip())
            if name_input:
                tickers_input[ticker_type] = name_input

            if len(best_ticker_matches["bestMatches"]) == 0:
                self.error_message = f'Your input "{ticker_value}" does not exist'

            # filter out invalid tickers
            better_matches = []
            for match in range(0, len(best_ticker_matches["bestMatches"])):
                if "." not in best_ticker_matches["bestMatches"][match]["1. symbol"] and "-" not in \
                        best_ticker_matches["bestMatches"][match]["1. symbol"]:
                    better_matches.append(best_ticker_matches["bestMatches"][match]["1. symbol"])

            if len(better_matches) == 0:
                self.error_message = f'Please enter ticker instead of "{ticker}"'
            else:
                self.error_message = better_matches[0]

        # checks if two tickers are the same
        if tickers_input

        return tickers_input


    # checks if two tickers are the same for comparison
    def check_same_tickers(ticker1: str, ticker2: str):
        if ticker1 == ticker2:
            return "Please input two different tickers"


    def check_raw_data(ticker_raw_data: dict) -> str:
        for raw_data_dict in ticker_raw_data:
            if not raw_data_dict:
                return "Inputted ticker does not have enough data to display"
