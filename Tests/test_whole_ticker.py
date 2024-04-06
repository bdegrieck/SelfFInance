from BackEnd.companyData import CompanyData
from BackEnd.errors import valid_ticker_input, get_formatted_ticker
from BackEnd.news import News


class TestWholeTicker:

    # purpose of this method is to test random instances of user input to debug issues
    def test_ticker(self):
        input = "kroger"
        ticker = get_formatted_ticker(ticker=input)
        #
        # company_data = CompanyData(ticker)
        # company_df = company_data.ticker_df_data
        company_news = News(ticker=ticker)
        print(company_news)


