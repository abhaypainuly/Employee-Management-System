from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

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

@home.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        # Redirecting to normal dashboard for non admin users
        return redirect(url_for("home.dashboard"))

    return render_template("home/admin_dashboard.html", title="Admin Dashboard")