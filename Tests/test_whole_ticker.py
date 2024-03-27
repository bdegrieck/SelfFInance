from BackEnd.companyData import CompanyData
from BackEnd.errors import valid_ticker_input, get_formatted_ticker
from BackEnd.news import News


class TestWholeTicker:

    def test_ticker(self):
        input = "google"
        assert valid_ticker_input(ticker=input) is None
        ticker = get_formatted_ticker(ticker=input)

        company_data = CompanyData(ticker)
        company_df = company_data.ticker_df_data
        company_news = News(ticker=ticker)
        print(company_news)


