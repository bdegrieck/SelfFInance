from flask import Blueprint, render_template, request
from BackEnd.user import User

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/submit", methods=["POST"])
def get_input():
    ticker = request.form["stockTicker"]
    micro = request.form["micro"]
    endpoints = request.form.getlist("endpoints")
    user_input = User(ticker, micro, endpoints)
    return render_template("tickerinfo.html", ticker=user_input.input_ticker, ticker_data=user_input.user_main_ticker.ticker_html_data)
