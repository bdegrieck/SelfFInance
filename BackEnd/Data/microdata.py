from BackEnd.Data.api import get_raw_api_data, get_micro_endpoints, get_micro_dfs


class MicroData:
    def __init__(self):
        endpoints = get_micro_endpoints()
        raw_data = get_raw_api_data(endpoints=endpoints)
        self.micro_df_data = get_micro_dfs(raw_data=raw_data)
