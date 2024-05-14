from BackEnd.Data.microdata import MicroData
from BackEnd.error import TickerDoesNotExist, EnterTickerInstead, SameTickers
from BackEnd.formatinput import UserInput
from BackEnd.user import User


class TestWholeTicker:
    # purpose of this test is to test random instances for debugging not part of phase 4
    def test_ticker(self):
        try:
            user_input = UserInput({
                "Ticker Input": ["AAPL"],
            })
            user_data = User(user_input=user_input)
            print(user_data)

        except (TickerDoesNotExist, EnterTickerInstead, SameTickers) as error:
            print(error)



