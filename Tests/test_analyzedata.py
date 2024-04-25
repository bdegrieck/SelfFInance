from BackEnd.datadifferentials import DataDifferentials
from BackEnd.companydata import CompanyData
import pandas as pd


class TestAnaylzeData:

    def test_anaylzedata(self):
        ticker = "AAPL"
        company = CompanyData(ticker=ticker)
        # company.company_prices.index = pd.to_datetime(company.company_prices.index)
        # print(company)
        analytics = DataDifferentials(company=company)
        print(company)




