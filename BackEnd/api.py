import requests

from BackEnd.error import InsufficientData


class API:

    def __init__(self, endpoints: dict, ticker: str = "MicroData"):
        self.ticker = ticker
        self.raw_data = self.get_raw_api_data(endpoints=endpoints)

    # get raw data endpoints are passed in
    def get_raw_api_data(self, endpoints: dict) -> dict:
        raw_data = {}
        for data_description, endpoint_url in endpoints.items():
            raw_data[data_description] = requests.get(url=endpoint_url).json()
        self.check_raw_data(ticker_raw_data=raw_data)
        return raw_data

    # tickers that the api cannot understand when inputting full company name instead of ticker
    def check_raw_data(self, ticker_raw_data: dict) -> str:
        for raw_data_dict in ticker_raw_data:
            if not raw_data_dict:
                InsufficientData(f"Inputted ticker: {self.ticker} does not have enough data to display")
