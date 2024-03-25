from flask import Blueprint, render_template, request, flash, redirect, url_for

from BackEnd.companyData import CompanyData
from BackEnd.compare import Compare
from BackEnd.microData import MicroData
from BackEnd.news import News
from BackEnd.errors import get_formatted_ticker, validate_user_input, validate_endpoints, check_same_tickers, \
    valid_ticker_input

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/tickerdata", methods=["POST"])
def get_input():
    user_ticker_main_input = {
        "Ticker Input": request.form.get("stockTicker"),
        "Microeconomic Input": request.form.get("micro"),
        "News Input": request.form.get("news")
    }

    endpoints_input = {
        "Company Overview + Price": "companyOverview" in request.form.getlist("companyOverview"),
        "EPS": "priceAndEPS" in request.form.getlist("priceAndEPS"),
        "Balance Sheet": "balanceSheet" in request.form.getlist("balanceSheet")
    }

    # checks user_ticker_main_input and displays error
    error_message = validate_user_input(user_input=user_ticker_main_input)
    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    # checks endpoints and displays error
    error_message = validate_endpoints(user_input=endpoints_input)
    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    error_message = valid_ticker_input(user_ticker_main_input["Ticker Input"])
    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    ticker_input = get_formatted_ticker(user_ticker_main_input["Ticker Input"])

    if ticker_input == f'Enter ticker instead of "{user_ticker_main_input["Ticker Input"]}"':
        flash(ticker_input)
        return redirect(url_for("views.home"))

    ticker_data = CompanyData(ticker=ticker_input)
    user_ticker_news = News(ticker=ticker_input)

    return render_template(
        template_name_or_list="tickerinfo.html",
        ticker=ticker_input,
        ticker_data=ticker_data.ticker_df_data,
        endpoints=endpoints_input,
        micro=user_ticker_main_input["Microeconomic Input"],
        news_input=user_ticker_main_input["News Input"],
        news_link=user_ticker_news.news,
        error_message=error_message,
        prices_dates=[date for date in ticker_data.ticker_df_data["ticker_prices_df"]['Close'][::-1].index],
        prices_values=[row for row in ticker_data.ticker_df_data["ticker_prices_df"]['Close'][::-1]]
    )


@views.route("/comparedata", methods=["POST"])
def get_comparison_data():
    user_input_tickers = {
        "Ticker 1": request.form.get("ticker1"),
        "Ticker 2": request.form.get("ticker2")
    }

    # checks if both ticker fields were entered
    error_message = validate_user_input(user_input=user_input_tickers)
    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    ticker1 = get_formatted_ticker(user_input_tickers["Ticker 1"])
    ticker2 = get_formatted_ticker(user_input_tickers["Ticker 2"])

    if ticker1 == f'Enter ticker instead of "{user_input_tickers["Ticker 1"]}"':
        flash(ticker1)
        return redirect(url_for("views.home"))

    if ticker2 == f'Enter ticker instead of "{user_input_tickers["Ticker 2"]}"':
        flash(ticker2)
        return redirect(url_for("views.home"))

    error_message = check_same_tickers(ticker1=ticker1, ticker2=ticker2)

    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    ticker1_data = CompanyData(ticker=ticker1)
    ticker2_data = CompanyData(ticker=ticker2)

    comparison_data = Compare(main_ticker_data=ticker1_data, second_ticker_data=ticker2_data)

    return render_template(
        template_name_or_list="comparedata.html",
        comparison_data=comparison_data.data_comparison,
        ticker1=ticker1,
        ticker2=ticker2,
        error_message=error_message
    )


@views.route("/compare")
def get_comparison_input():
    return render_template(
        template_name_or_list="compare.html"
    )


@views.route("/micro")
def get_micro():
    micro_data_input = MicroData()

    return render_template(
        template_name_or_list="micro.html",

        real_gdp_dates=[date for date in micro_data_input.micro_df_data["real_gdp_df"][::-1].index],
        real_gdp_values=[value for value in micro_data_input.micro_df_data["real_gdp_df"]["Real GDP"][::-1]],

        cpi_dates=[date for date in micro_data_input.micro_df_data["cpi_df"][::-1].index],
        cpi_values=[value for value in micro_data_input.micro_df_data["cpi_df"]["CPI"][::-1]],

        inflation_dates=[date for date in micro_data_input.micro_df_data["inflation_df"][::-1].index],
        inflation_values=[value for value in micro_data_input.micro_df_data["inflation_df"]["Inflation Rate"][::-1]],

        fed_dates=[date for date in micro_data_input.micro_df_data["federal_funds_rate_df"][::-1].index],
        fed_values=[value for value in micro_data_input.micro_df_data["federal_funds_rate_df"]["Federal Funds Rate"][::-1]],

        retail_dates=[date for date in micro_data_input.micro_df_data["retail_sales_df"][::-1].index],
        retail_values=[value for value in micro_data_input.micro_df_data["retail_sales_df"]["Retail Sales"][::-1]],

        unemployment_dates=[date for date in micro_data_input.micro_df_data["unemployment_rate_df"][::-1].index],
        unemployment_values=[value for value in micro_data_input.micro_df_data["unemployment_rate_df"]["Unemployment Rate"][::-1]],
    )
