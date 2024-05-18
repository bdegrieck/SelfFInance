from BackEnd.error import InsufficientData


# tickers that the api cannot understand when inputting full company name instead of ticker
def check_raw_data(ticker_raw_data: dict):
    for raw_data_dict in ticker_raw_data:
        if not raw_data_dict:
            InsufficientData(f"Inputted ticker: {raw_data_dict} does not have enough data to display")
