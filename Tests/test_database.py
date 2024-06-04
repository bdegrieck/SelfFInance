from BackEnd.Data.companydata import CompanyData
from BackEnd.user import UserInput
from BackEnd.database import DBConn

class TestDBConn:

    def test_connection(self):
        input = UserInput(tickers=["AAPL"])
        ticker_data = CompanyData(ticker=input.tickers[0])

        db_manager = DBConn()
        data_base = "appledata"
        db_conn = db_manager.get_connection(data_base=data_base)
        db_manager.post_whole_company_data(company_raw_data=ticker_data, db_connection=db_conn)

