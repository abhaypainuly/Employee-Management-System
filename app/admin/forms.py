from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role

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

class EmployeeAsignForm(FlaskForm):
    """
    Form to assign employees to department and roles!
    """
    department = QuerySelectField(
        query_factory=lambda : Department.query.all(),
        label = "Department"
    )

    role = QuerySelectField(
        query_factory=lambda : Role.query.all(),
        label = "Role"
    )

    submit = SubmitField("Submit")