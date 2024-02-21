from BackEnd.data import endpoint_company_request, endpoint_micro_request, get_raw_api_data, get_spec_api_data, get_html


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
    company_endpoints = endpoint_company_request(ticker=user_input_ticker, api_key=api_key)
    micro_endpoints = endpoint_micro_request(ticker=user_input_ticker, api_key=api_key)

    # get raw
    company_raw_data = get_raw_api_data(endpoints=company_endpoints)
    micro_raw_data = get_raw_api_data(endpoints=micro_endpoints)

    # get real data
    spec_company_data = get_spec_api_data(raw_data=company_raw_data)
    spec_micro_data = get_spec_api_data(raw_data=micro_raw_data)

    # format data to html
    company_html = get_html(spec_data=spec_company_data)
    micro_html = get_html(spec_data=spec_micro_data)