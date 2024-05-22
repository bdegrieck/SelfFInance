from BackEnd.Data.calender import EarningsCalender
from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.earningsdata import EarningsData
from BackEnd.Data.microdata import MicroData
from BackEnd.Data.techindicators import TechnicalIndicators


class TestEarningsCalender:

    def test_data(self):
        ticker = "AAPL"
        company_data = CompanyData(ticker=ticker)
        technical_analysis_data = TechnicalIndicators(ticker=ticker)
        micro_data = MicroData()
        earnings = EarningsData(micro_data=micro_data, stock_data=company_data, technical_analysis_data=technical_analysis_data)
        print(earnings)