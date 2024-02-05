from BackEnd.data import endpoint_company_request, get_api_data


class Main:
    user_input_ticker = input("Enter a ticker:")
    api_key = "5Q940ZTYF4PPW5S4"
    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}"
    micro_input = input("Dop you want microecomic data?:")
    if micro_input.lower() == "yes" or "y":
        micro_input = True

    company_data = endpoint_company_request(api_key=api_key)
    company_data_retrieval = get_api_data(company_data)
    print(company_data)
