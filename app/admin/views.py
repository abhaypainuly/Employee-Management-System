from flask import render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from . import admin
from .. import db
from ..models import Department
from .forms import DepartmentForm


def check_admin():
    """
    Gives access to admin only!
    """
    if not current_user.is_admin:
        abort(403)


@admin.route("/departments", methods=["GET", "POST"])
@login_required
def department_list():
    """
    If user is admin, then renders /admin/department template!
    """
    check_admin()
    departments = Department.query.all()

    return render_template("admin/departments/departments.html", departments = departments, title="Departments")


@admin.route("/departments/add", methods=["GET", "POST"])
@login_required
def department_add():
    """
    If user is admin, renders template to add departments!
    """
    check_admin()
    add_department = True
    form = DepartmentForm()
    
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)

        try:
            # Adding to the database
            db.session.add(department)
            db.session.commit()
            flash("Department successfully added!")
            return redirect(url_for("admin.department_list"))

        except:
            flash("Department was not added as it already exists!")        

    return render_template("admin/departments/department.html", action="Add", add_department=add_department, form=form, title="Add Department")


@admin.route("/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def department_edit(id):
    """
    If user is admin, renders template to edit department!
    """
    check_admin()
    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)

    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        
        try:
            # Commiting to the database
            db.session.commit()
            flash("Department Edited Succesfully!")

            return redirect(url_for("admin.department_list"))

        except:
            flash("Failed to edit Department as it Already Exists!")

    form.name.data = department.name
    form.description.data = department.description
    return render_template("admin/departments/department.html", action="Edit", add_department=add_department, form=form, department=department, title="Edit Department")


@admin.route("/department/delete/<int:id>", methods=["GET", "POST"])
@login_required
def department_delete(id):
    """
    If user is admin, renders template to delete department!
    """
    check_admin()
    
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash("Department Deleted!")

    return redirect(url_for("admin.department_list"))