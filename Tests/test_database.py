from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.techindicators import TechnicalIndicators
from BackEnd.user import UserInput
from BackEnd.database import DBConn

class TestDBConn:

    def test_connection(self):
        input = UserInput(tickers=["AAPL"])
        technical_analysis_data = TechnicalIndicators(ticker=input.tickers[0]).dfs

        db_manager = DBConn()
        data_base = "appledata"
        db_conn = db_manager.get_connection(data_base=data_base)
        if db_conn:
             db_manager.post_all_technical_indicator_data(technical_indicators=technical_analysis_data, db_conn=db_conn, db_name="appledata")
             db_manager.get_all_technical_df_data(db_conn=db_conn)

