import requests
from flask import flash, redirect, url_for, request

from BackEnd import constants


def get_formatted_ticker(ticker: str) -> str:
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={constants.API_KEY}'
    ticker = requests.get(url).json()["bestMatches"][0]["1. symbol"]
    return ticker


def validate_user_input(user_input: dict):
    for input_type, input_value in user_input.items():
        if not input_value:
            return f"{input_type}: is empty"


def validate_endpoints(user_input: dict):
    if not any(user_input.values()):
        return f'Please select at least one options:{list(user_input.keys())}'
