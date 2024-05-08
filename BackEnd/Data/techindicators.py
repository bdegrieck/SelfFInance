from BackEnd.Data.api import get_raw_api_data, get_technical_indicator_endpoints, get_technical_indicator_dfs


class TechnicalIndicators:

    def __init__(self, ticker: str):
        endpoints = get_technical_indicator_endpoints(ticker=ticker)
        raw_data = get_raw_api_data(endpoints=endpoints)
        self.technical_indicator_data = get_technical_indicator_dfs(indicator_raw_data=raw_data)
