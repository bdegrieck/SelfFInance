from flask import Blueprint, render_template, request, flash, redirect, url_for

from BackEnd.Data.calender import EarningsCalender
from BackEnd.error import TickerDoesNotExist, EnterTickerInstead, SameTickers, InsufficientData, EmptyInput
from BackEnd.user import User
from BackEnd.formatinput import UserInput
from BackEnd.Data.tickercomparison import TickerComparison
from BackEnd.Data.microdata import MicroData

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/tickerdata", methods=["POST"])
def get_input():
    try:
        user_input = UserInput({"Ticker Input": [request.form.get("stockTicker")]})

        calender_home = request.form.get("calenderRoute")

        user_data = User(user_input)

        return render_template(
            template_name_or_list="tickerinfo.html",
            calender_home=calender_home,
            ticker=user_data.formatted_tickers[0],
            ticker_data=user_data.company_data[0],
            news_link=user_data.news_data.news,
            prices_dates=[f"{date.month}-{date.day}-{date.year}" for date in user_data.company_data[0].company_dfs.stock_data_df["close"][::-1].index],
            prices_values=[row for row in user_data.company_data[0].company_dfs.stock_data_df['close'][::-1]]
        )

    except (TickerDoesNotExist, EnterTickerInstead, SameTickers, InsufficientData, EmptyInput) as error:
        flash(str(error))
        return redirect(url_for("views.home"))


@views.route("/comparedata", methods=["POST"])
def get_comparison_data():
    try:
        user_input = UserInput({"Ticker Input": [request.form.get("ticker1"), request.form.get("ticker2")]})

        user_data = User(user_input=user_input)

        comparison_data = TickerComparison(main_ticker_data=user_data.company_data[0], second_ticker_data=user_data.company_data[1])

        return render_template(
            template_name_or_list="comparedata.html",
            comparison_data=comparison_data.data_comparison,
            ticker1=user_data.formatted_tickers[0],
            ticker2=user_data.formatted_tickers[1],
        )

    except (TickerDoesNotExist, EnterTickerInstead, SameTickers, InsufficientData, EmptyInput) as error:
        flash(str(error))
        return redirect(url_for("views.home"))


@views.route("/compare")
def get_comparison_input():
    return render_template(
        template_name_or_list="compare.html"
    )


@views.route("/micro", methods=["POST"])
def get_micro():
    micro_data = MicroData()

    ticker = request.form.get("stockTicker")

    return render_template(
        template_name_or_list="micro.html",

        ticker=ticker,

        real_gdp_dates=[f"{date.month}-{date.day}-{date.year}" for date in micro_data.real_gdp[::-1].index],
        real_gdp_values=[value for value in micro_data.real_gdp["realGDP"][::-1]],

        cpi_dates=[f"{date.month}-{date.day}-{date.year}" for date in micro_data.cpi[::-1].index],
        cpi_values=[value for value in micro_data.cpi["cpi"][::-1]],

        inflation_dates=[f"{date.month}-{date.day}-{date.year}" for date in micro_data.inflation_rates[::-1].index],
        inflation_values=[value for value in micro_data.inflation_rates["inflationRate"][::-1]],

        fed_dates=[f"{date.month}-{date.day}-{date.year}" for date in micro_data.interest_rates[::-1].index],
        fed_values=[value for value in micro_data.interest_rates["interestRate"][::-1]],

        retail_dates=[f"{date.month}-{date.day}-{date.year}" for date in micro_data.retail_sales[::-1].index],
        retail_values=[value for value in micro_data.retail_sales["retailSales"][::-1]],

        unemployment_dates=[f"{date.month}-{date.day}-{date.year}" for date in micro_data.unemployment_rates[::-1].index],
        unemployment_values=[value for value in micro_data.unemployment_rates["unemploymentRate"][::-1]],
    )


@views.route("/calenderhome")
def calender_home():
    return render_template(
        template_name_or_list="calenderhome.html"
    )


@views.route("/calenderinfo", methods=["POST"])
def get_upcoming_calender():
    user_input = UserInput({"Ticker Input": [request.form.get("calenderInput")]})
    earnings_calenders = EarningsCalender(ticker=user_input.raw_tickers_input[0])

    return render_template(
        template_name_or_list="calenderinfo.html",
        ticker=user_input.raw_tickers_input[0],
        upcoming_earnings_calender=earnings_calenders.upcoming_earnings_df,
        upcoming_earnings_calender_company=earnings_calenders.company_earnings_df
    )
