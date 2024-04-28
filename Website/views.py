from flask import Blueprint, render_template, request, flash, redirect, url_for

from BackEnd.error import TickerDoesNotExist, EnterTickerInstead, SameTickers, InsufficientData, NoNews, EmptyInput
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
        user_input = UserInput({
            "Ticker Input": [request.form.get("stockTicker")],
            "Microeconomic Input": request.form.get("micro"),
            "News Input": request.form.get("news"),
            "Endpoints Input": {
                "Company Overview + Price": "companyOverview" in request.form.getlist("companyOverview"),
                "EPS": "priceAndEPS" in request.form.getlist("priceAndEPS"),
                "Balance Sheet": "balanceSheet" in request.form.getlist("balanceSheet")
            }
        })

        user_data = User(user_input)

        return render_template(
            template_name_or_list="tickerinfo.html",
            ticker=user_data.formatted_tickers[0],
            ticker_data=user_data.company_data[0].ticker_df_data,
            endpoints=user_input.endpoints_input,
            micro=user_input.micro_input,
            news_input=user_input.news_input,
            news_link=user_data.news_data.news,
            prices_dates=[date for date in user_data.company_data[0].ticker_df_data["ticker_prices_df"]['Close'][::-1].index],
            prices_values=[row for row in user_data.company_data[0].ticker_df_data["ticker_prices_df"]['Close'][::-1]]
        )

    except (TickerDoesNotExist, EnterTickerInstead, SameTickers, InsufficientData, NoNews, EmptyInput) as error:
        flash(str(error))
        return redirect(url_for("views.home"))


@views.route("/comparedata", methods=["POST"])
def get_comparison_data():
    try:
        user_input = UserInput({
            "Ticker Input": [request.form.get("ticker1"), request.form.get("ticker2")],
            "Microeconomic Input": "Empty",
            "News Input": "Empty",
            "Endpoints Input": {
                "Company Overview + Price": "Empty",
                "EPS": "Empty",
                "Balance Sheet": "Empty"
            }
        })

        user_data = User(user_input=user_input)

        comparison_data = TickerComparison(main_ticker_data=user_data.company_data[0], second_ticker_data=user_data.company_data[1])

        return render_template(
            template_name_or_list="comparedata.html",
            comparison_data=comparison_data.data_comparison,
            ticker1=user_data.formatted_tickers[0],
            ticker2=user_data.formatted_tickers[1],
        )

    except (TickerDoesNotExist, EnterTickerInstead, SameTickers, InsufficientData, NoNews, EmptyInput) as error:
        flash(str(error))
        return redirect(url_for("views.home"))


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
