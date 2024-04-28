from BackEnd.Data.companydata import CompanyData
from BackEnd.formatinput import UserInput, format_ticker_input
from BackEnd.Data.news import News


class User:
    def __init__(self, user_input: type(UserInput)):
        self.formatted_tickers = format_ticker_input(user_input_tickers=user_input.raw_tickers_input)
        self.company_data = self.get_company_data(tickers=self.formatted_tickers)
        self.news_data = News(self.formatted_tickers[0])

    def get_company_data(self, tickers: list) -> list:
        company_data = []
        for ticker in tickers:
            company_data.append(CompanyData(ticker=ticker))
        return company_data
