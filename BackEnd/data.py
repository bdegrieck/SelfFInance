import numpy as np
import requests


# get raw data endpoints are passed in
def get_raw_api_data(endpoints: dict) -> dict:
    raw_data = {}
    for data_description, endpoint_url in endpoints.items():
        raw_data[data_description] = requests.get(url=endpoint_url).json()
    return raw_data


# format spec data dfs to html to frontend
def get_html(df_data: dict) -> dict:
    html_data = {}
    for df, data in df_data.items():
        html_data[df] = data.to_html(classes="table table-striped")
    return html_data


def get_clean_data(df_data: dict):
    for data_category, df_value in df_data.items():
        for column in df_value.columns:
            df_data[data_category][column] = df_value[column].fillna(0).replace(to_replace=["None", np.nan], value=0)
            try:
                df_data[data_category][column] = df_data[data_category][column].astype(float)
            except:
                pass
    return df_data


def remove_empties(df_data: dict):
    for data_category, df_value in df_data.items():
        df_data[data_category] = df_value[df_value.index.notna()]
    return df_data
