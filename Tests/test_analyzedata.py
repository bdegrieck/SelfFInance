from BackEnd.Data.companydata import CompanyData
from BackEnd.Data.reportdifferences import ReportDifferences
from BackEnd.SFBuddy import OrdinaryLeastSquares
from BackEnd.formatinput import UserInput
from BackEnd.user import User


class TestAnaylzeData:

    def test_anaylzedata(self):
        user_input = UserInput({"Ticker Input": ["AAPL"]})

        user_data = User(user_input=user_input)
        company_data = user_data.company_data[0]
        company_differences = ReportDifferences(company_balance_sheet=company_data.company_balance_sheet, company_eps=company_data.company_eps, company_prices=company_data.company_prices)
        models = OrdinaryLeastSquares(company=user_data.company_data[0])
        print(models)




