from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.earningsdata import EarningsData
from BackEnd.Models.SFBuddy import OrdinaryLeastSquares
from BackEnd.formatinput import UserInput
from BackEnd.user import User


class TestAnaylzeData:

    def test_anaylzedata(self):
        company_data = CompanyData(ticker="AAPL")
        company_differences = EarningsData(stock_data=company_data)
        print(company_differences)




