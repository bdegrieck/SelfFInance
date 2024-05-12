from BackEnd.Data.techindicators import TechnicalIndicators


class TestTechIndicators:

    def test_indicators(self):
        ticker = "AAPL"
        tech_ind = TechnicalIndicators(ticker=ticker)