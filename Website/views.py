from flask import Blueprint, render_template, request

from BackEnd.companyData import CompanyData
from BackEnd.compare import Compare
from BackEnd.microData import MicroData
from BackEnd.news import News

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/submit", methods=["POST"])
def get_input():
    ticker = request.form["stockTicker"]
    micro = request.form.get("micro")
    news = request.form.get("news")
    endpoints = {
        "Company Overview": "companyOverview" in request.form.getlist("companyOverview"),
        "priceAndEPS": "priceAndEPS" in request.form.getlist("priceAndEPS"),
        "Balance Sheet": "balanceSheet" in request.form.getlist("balanceSheet")
    }
    user_input = CompanyData(ticker=ticker)
    user_ticker_news = News(ticker=user_input.ticker)
    return render_template(
        template_name_or_list="tickerinfo.html",
        ticker=user_input.ticker,
        ticker_data=user_input.ticker_df_data,
        endpoints=endpoints,
        micro=micro,
        news_input=news,
        news_link=user_ticker_news.news
    )


@views.route("/comparedata", methods=["POST"])
def get_comparison_datat():
    ticker1 = request.form.get("ticker1")
    ticker2 = request.form.get("ticker2")
    ticker1_data = CompanyData(ticker=ticker1)
    ticker2_data = CompanyData(ticker=ticker2)
    comparison_data = Compare(main_ticker_data=ticker1_data, second_ticker_data=ticker2_data)
    return render_template(
        template_name_or_list="comparedata.html",
        comparison_data=comparison_data.data_comparison,
        ticker1=ticker1,
        ticker2=ticker2
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

