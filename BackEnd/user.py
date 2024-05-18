from typing import Optional, List

import requests
from pydantic import BaseModel, validator

from BackEnd import constants
from BackEnd.Data.companydata import CompanyData
from BackEnd.error import TickerDoesNotExist, EnterTickerInstead, SameTickers, EmptyInput


class UserInput(BaseModel):
    tickers: Optional[List[str]]

    @validator("tickers", pre=True)
    def format_ticker_input(cls, tickers):
        formatted_tickers = []
        check_for_blank_ticker_input(user_input_tickers=tickers)
        for ticker in tickers:
            url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={constants.API_KEY}'
            ticker_list = requests.get(url).json()

            name_input = check_extraneous_tickers(input_name=ticker.lower().strip())
            if name_input:
                formatted_tickers.append(name_input)
                continue

            if len(ticker_list["bestMatches"]) == 0:
                raise TickerDoesNotExist(f'Your input "{ticker}" does not exist')

            # filter out invalid tickers
            better_matches = []
            for match in range(0, len(ticker_list["bestMatches"])):
                if "." not in ticker_list["bestMatches"][match]["1. symbol"] and "-" not in \
                        ticker_list["bestMatches"][match]["1. symbol"]:
                    better_matches.append(ticker_list["bestMatches"][match]["1. symbol"])

            if len(better_matches) == 0:
                raise EnterTickerInstead(f'Please enter ticker instead of "{ticker}"')
            else:
                formatted_tickers.append(better_matches[0])

        # checks if tickers are the same for comparison
        if len(tickers) > 1 and tickers[0] == tickers[1]:
            raise SameTickers("Please input two different tickers")

        return formatted_tickers


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


def get_company_data(tickers: list) -> list:
    company_data = []
    for ticker in tickers:
        company_data.append(CompanyData(ticker=ticker))
    return company_data
