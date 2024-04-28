import requests

from BackEnd import constants
from BackEnd.error import NoNews


class News:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.ticker}&apikey={constants.API_KEY}'
        self.news = self.get_news()

    # calls api to return most recent news article of ticker
    def get_news(self) -> str:
        try:
            news_link = requests.get(url=self.url).json()
            if news_link["Information"]:
                return " "
            news_feed = news_link["feed"]
            # checks for a more relevant article with ticker in title
            for news_index in range(len(news_feed)):
                if self.ticker in news_feed[news_index]["title"] or self.ticker in news_feed[news_index]["url"]:
                    return news_feed[news_index]["url"]
            return news_feed[00]["url"]
        except:
            raise NoNews(f'There are no relevant news for your ticker: "{self.ticker}"')
