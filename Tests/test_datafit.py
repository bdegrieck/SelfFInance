from BackEnd.Data.companydata import CompanyData
from BackEnd.Models.modelPrep import DataFit


class TestModelFit:

    def test_model_fit(self):
        company_data = CompanyData(ticker="AAPL")
        DataFit(stock_data=company_data)
