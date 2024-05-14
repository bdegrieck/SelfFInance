from BackEnd.Data.calender import EarningsCalender
from BackEnd.Models.modelPrep import linear_model_eps_calender_fit


class TestCalenderEarnings:

    def test_calenders(self):

        ticker = "AAPL"
        earnings_calender = EarningsCalender(ticker=ticker)
        prep = linear_model_eps_calender_fit(calender_df=earnings_calender)
