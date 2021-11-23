from flask import render_template, flash
from flask_login import login_required

from . import home

@home.route("/")
def homepage():
    """
    Renders the homepage template!
    """
    return render_template("home/index.html", title="Welcome")

@home.route("/dashboard")
@login_required
def dashboard():
    """
    Renders the dashboard template!
    """
    return render_template("home/dashboard.html", title="Dashboard")