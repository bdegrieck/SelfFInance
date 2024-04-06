import requests

from BackEnd import constants


class News:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.api_key = constants.API_KEY
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.ticker}&apikey={self.api_key}'
        self.news = self.get_news()

    # calls api to return most recent news article of ticker
    def get_news(self) -> str:
        news_link = requests.get(url=self.url).json()
        news_feed = news_link["feed"]
        if len(news_feed) == 0:
            return f'There are no relevant news for your ticker: "{self.ticker}"'

        # checks for a more relevant article with ticker in title
        for news_index in range(len(news_feed)):
            if self.ticker in news_feed[news_index]["title"] or self.ticker in news_feed[news_index]["url"]:
                return news_feed[news_index]["url"]

        return news_feed[00]["url"]
