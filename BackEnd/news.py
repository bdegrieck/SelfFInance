import requests


class News:
    def __init__(self, ticker: str, api_key: str):
        self.ticker = ticker
        self.api_key = api_key
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.ticker}&apikey={self.api_key}'

    def getNews(self):
        news_link = requests.get(url=self.url).json()["feed"][00]["url"]
        return news_link
