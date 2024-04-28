from BackEnd.Data.datadifferentials import DataDifferentials
from BackEnd.Data.companydata import CompanyData


class TestAnaylzeData:

    def test_anaylzedata(self):
        ticker = "AAPL"
        company = CompanyData(ticker=ticker)
        # company.company_prices.index = pd.to_datetime(company.company_prices.index)
        # print(company)
        analytics = DataDifferentials(company=company)
        print(company)




