from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    """
    Login Form class!
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    """
    Registration Form class!
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Register!")