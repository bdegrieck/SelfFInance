import numpy as np
import requests
from BackEnd.error import check_raw_data


# get raw data endpoints are passed in
def get_raw_api_data(endpoints: dict) -> dict:
    raw_data = {}
    for data_description, endpoint_url in endpoints.items():
        raw_data[data_description] = requests.get(url=endpoint_url).json()
    check_raw_data(ticker_raw_data=raw_data)
    return raw_data


# cleans dataframe to remove nan values and 'None'
def get_clean_data(df_data: dict) -> dict:
    for data_category, df_value in df_data.items():
        for column in df_value.columns:
            df_data[data_category][column] = df_value[column].fillna(0).replace(to_replace=["None", np.nan], value=0)
            try:
                df_data[data_category][column] = df_data[data_category][column].astype(float)
            except:
                pass
    return df_data


# removes rows of data that have 0 as date
def remove_empties(df_data: dict) -> dict:
    for data_category, df_value in df_data.items():
        df_data[data_category] = df_value[df_value.index.notna()]
    return df_data
