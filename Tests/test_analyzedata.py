from BackEnd.Data.companydata import CompanyData
from BackEnd.Models.SFBuddy import LinearModels
from BackEnd.Models.modelPrep import DataFit


class TestAnaylzeData:

    def test_anaylzedata(self):
        company_data = CompanyData(ticker="AAPL")
        model_data = DataFit(stock_data=company_data)
        linear_model_stat = LinearModels(model_data=model_data.linear_model_dict)




