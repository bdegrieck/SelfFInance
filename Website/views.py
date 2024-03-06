from flask import Blueprint, render_template, request

views = Blueprint("views", __name__)

@views.route("/")
def get_input():
    ticker = ""
    if request.form:
        ticker = request.form

    return render_template("home.html", tickerinput=ticker)

@views.route("/ticker")
def post_data(html_data: str):
    return render_template("tickerinfo.html", data_html=html_data)



