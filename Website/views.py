from flask import Blueprint, render_template, request
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
    user_input = User(ticker)
    return render_template(
        "tickerinfo.html",
                ticker=user_input.input_ticker,
                ticker_data=user_input.main_ticker_data.ticker_df_data,
                endpoints=endpoints,
                micro=micro)

@views.route("/micro", methods=["POST"])
def get_micro():
    micro = request.form.get("micro")

