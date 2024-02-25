from BackEnd.data import get_endpoint_company, get_endpoint_micro, get_raw_api_data, get_company_df_data, get_html, get_micro_df_data


# getting user data for ticker and economic data
def get_user_input():
    # user_input_ticker = input("Enter a ticker:")
    user_input_ticker = "AAPL"

    # micro_input = input("Dop you want microecomic data?:")
    # if micro_input.lower() == "yes" or "y":
    #     micro_input = True
    return user_input_ticker


class Main:
    api_key = "CRU63X7J4COJ46F2"
    user_input_ticker = get_user_input()

    # get url endpoints
    company_endpoints = get_endpoint_company(ticker=user_input_ticker, api_key=api_key)
    micro_endpoints = get_endpoint_micro(ticker=user_input_ticker, api_key=api_key)

    # get raw
    company_raw_data = get_raw_api_data(endpoints=company_endpoints)
    micro_raw_data = get_raw_api_data(endpoints=micro_endpoints)

    # get real data
    company_dfs = get_company_df_data(raw_company_data=company_raw_data)
    micro_dfs = get_micro_df_data(raw_micro_data=micro_raw_data)

    # format data to html
    company_html = get_html(df_data=company_dfs)
    micro_html = get_html(df_data=micro_dfs)