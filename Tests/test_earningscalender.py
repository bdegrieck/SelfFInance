from BackEnd.Data.calender import EarningsCalender
from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.earningsdata import EarningsData
from BackEnd.Data.microdata import MicroData
from BackEnd.Data.techindicators import TechnicalIndicators


class TestEarningsCalender:

    def test_data(self):
        ticker = "AAPL"
        company_data = CompanyData(ticker=ticker)
        report_dates = company_data.company_dfs.eps_df["reportDate"]
        get_price_differences