from BackEnd.Data.reportdifferences import ReportDifferences
from BackEnd.Data.companydata import CompanyData
from BackEnd.SFBuddy import OrdinaryLeastSquares


class TestAnaylzeData:

    def test_anaylzedata(self):
        ticker = "AAPL"
        company = CompanyData(ticker=ticker)
        models = OrdinaryLeastSquares(company=company)
        print(company)




