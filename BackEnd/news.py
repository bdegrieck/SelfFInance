import requests

from BackEnd import constants


class News:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.api_key = constants.API_KEY
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.ticker}&apikey={self.api_key}'
        self.news = self.get_news()

    def get_news(self) -> str:
        news_link = requests.get(url=self.url).json()["feed"][00]["url"]
        return news_link
