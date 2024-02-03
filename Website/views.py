from flask import Blueprint, render_template, request, flash, jsonify

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home", methods=["GET", "POST"])
def main_input():
    ticker = ""
    if request.form:
        ticker = request.form

    return render_template("home.html", tickerinput=ticker)


