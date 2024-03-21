from flask import Blueprint, render_template, request, flash, redirect, url_for

from BackEnd.companyData import CompanyData
from BackEnd.compare import Compare
from BackEnd.microData import MicroData
from BackEnd.news import News
from BackEnd.errors import get_formatted_ticker, validate_user_input, validate_endpoints

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/submit", methods=["POST"])
def get_input():
    error_message = None
    user_input = {
        "Ticker Input": request.form.get("stockTicker"),
        "Microeconomic Input": request.form.get("micro"),
        "News Input": request.form.get("news")
    }

    endpoints = {
        "Company Overview + Price": "companyOverview" in request.form.getlist("companyOverview"),
        "EPS": "priceAndEPS" in request.form.getlist("priceAndEPS"),
        "Balance Sheet": "balanceSheet" in request.form.getlist("balanceSheet")
    }

    error_message = validate_user_input(user_input=user_input)
    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    error_message = validate_endpoints(user_input=endpoints)
    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    ticker_input = get_formatted_ticker(user_input["Ticker Input"])

    ticker_data = CompanyData(ticker=ticker_input)
    user_ticker_news = News(ticker=ticker_input)

    return render_template(
        template_name_or_list="tickerinfo.html",
        ticker=ticker_input,
        ticker_data=ticker_data.ticker_df_data,
        endpoints=endpoints,
        micro=user_input["Microeconomic Input"],
        news_input=user_input["News Input"],
        news_link=user_ticker_news.news,
        error_message=error_message,
        dates_chart=[date for date in ticker_data.ticker_df_data["ticker_prices_df"]['Close'][::-1].index],
        prices_chart=[row for row in ticker_data.ticker_df_data["ticker_prices_df"]['Close'][::-1]]
    )


@views.route("/comparedata", methods=["POST"])
def get_comparison_data():
    user_input = {
        "Ticker 1": request.form.get("ticker1"),
        "Ticker 2": request.form.get("ticker2")
    }
    error_message = validate_user_input(user_input=user_input)
    if error_message:
        flash(error_message)
        return redirect(url_for("views.home"))

    ticker1 = get_formatted_ticker(user_input["Ticker 1"])
    ticker2 = get_formatted_ticker(user_input["Ticker 2"])
    ticker1_data = CompanyData(ticker=ticker1)
    ticker2_data = CompanyData(ticker=ticker2)
    comparison_data = Compare(main_ticker_data=ticker1_data, second_ticker_data=ticker2_data)

    return render_template(
        template_name_or_list="comparedata.html",
        comparison_data=comparison_data.data_comparison,
        ticker1=ticker1,
        ticker2=ticker2,
        error_message = error_message
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
        microdata=micro_data_input.micro_df_data
    )
