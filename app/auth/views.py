from flask import render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .. import db
from ..models import Employee
from forms import LoginForm, RegisterForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Login users from /login page!
    """
    form = LoginForm()
    if form.validate_on_submit():        
        # Checking if user is registered or not
        employee =  Employee.query.filter_by(email=form.email.data).first()
        if employee is not None:
            if employee.verify_password(form.password.data): 
                # Log user In
                login_user(employee)

                # Redirecting to dashboard
                return redirect(url_for("home.dashboard"))
            else:
                flash("Incorrect Password!")
        else:
            flash("Invalid Email!")
    
    # Loading login tempalate
    return render_template("auth/login.html", form=form, title="Login")


@auth.route("/logout")
@login_required
def logout():
    """
    Logs out user!
    """
    logout_user()
    flash("You are sucessfully Logged out!")
    
    # Redirecting to login page
    return redirect(url_for("auth.login"))
    

@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    Register user from /register page!
    """
    form = RegisterForm()
    if form.validate_on_submit():
        
        # Checking if username already exist or not
        employee = Employee.query.filter_by(username=form.username.data).first()
        if employee is not None:
            
            # Checking if email already registered or not
            employee = Employee.query.filter_by(email=form.email.data).first()
            if employee is not None:
                # Creating the Employee class object
                employee = Employee(
                    email = form.email.data,
                    username = form.email.data,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    password = form.password.data
                )

                # Adding the user to database
                db.session.add(employee)
                db.session.commit()
            else:
                flash("Email already Registered!")
        else:
            flash("Username already exist!")

    # Rendering register template
    return render_template("auth/register.html", form=form, title="Register")