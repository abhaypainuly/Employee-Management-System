from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

class DepartmentForm(FlaskForm):
    """
    Department form for admin to edit!
    """
    name = StringField(
        "Name", 
        validators = [
            DataRequired()
        ]
    )
    description = StringField(
        "Description",
        validators = [
            DataRequired()
        ]
    )
    submit = SubmitField("Submit")

class RoleForm(FlaskForm):
    """
    Role Form for admin to edit!
    """
    name = StringField(
        "Name", 
        validators = [
            DataRequired()
        ]
    )
    description = StringField(
        "Description",
        validators = [
            DataRequired()
        ]
    )
    submit = SubmitField("Submit")

