import requests


# get raw data endpoints are passed in
def get_raw_api_data(endpoints: dict) -> dict:
    raw_data = {}
    for data_description, endpoint_url in endpoints.items():
        raw_data[data_description] = requests.get(url=endpoint_url).json()
    return raw_data


# format spec data dfs to html to frontend
def get_html(df_data: dict) -> dict:
    html_data = {}
    for df, data in df_data.items():
        html_data[df] = data.to_html(classes="table table-striped")
    return html_data


def get_ticker(ticker: str, api_key:str) -> str:
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={api_key}'
    ticker = requests.get(url).json()["bestMatches"][0]["1. symbol"]
    return ticker