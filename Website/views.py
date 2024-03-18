from flask import Blueprint, render_template, request

from BackEnd.companyData import CompanyData
from BackEnd.microData import MicroData
from BackEnd.user import User

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/submit", methods=["POST"])
def get_input():
    ticker = request.form["stockTicker"]
    micro = request.form.get("micro")
    endpoints = {
        "Company Overview": "companyOverview" in request.form.getlist("companyOverview"),
        "priceAndEPS": "priceAndEPS" in request.form.getlist("priceAndEPS"),
        "Balance Sheet": "balanceSheet" in request.form.getlist("balanceSheet")
    }
    user_input = CompanyData(ticker)
    return render_template(
        template_name_or_list="tickerinfo.html",
        ticker=user_input.ticker,
        ticker_data=user_input.ticker_df_data,
        endpoints=endpoints,
        micro=micro
    )


@views.route("/micro")
def get_micro():
    micro_data_input = MicroData()
    return render_template(
        template_name_or_list="micro.html",
        microdata=micro_data_input.micro_df_data
    )

