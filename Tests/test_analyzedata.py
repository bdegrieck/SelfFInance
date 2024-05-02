from BackEnd.Data.reportdifferences import ReportDifferences
from BackEnd.Data.companydata import CompanyData


class TestAnaylzeData:

    def test_anaylzedata(self):
        ticker = "AAPL"
        company = CompanyData(ticker=ticker)
        print(company)




