from flask import render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAsignForm

from .. import db
from ..models import Department, Role, Employee



def check_admin():
    """
    Gives access to admin only!
    """
    if not current_user.is_admin:
        abort(403)


@admin.route("/departments", methods=["GET"])
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
            # Issuing rollback
            db.session.rollback()
            flash("Department Already Exists!")        

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
            # Issuing rollback
            db.session.rollback()
            flash("Editting Department Failed!")

    form.name.data = department.name
    form.description.data = department.description
    return render_template("admin/departments/department.html", action="Edit", add_department=add_department, form=form, department=department, title="Edit Department")


@admin.route("/departments/delete/<int:id>", methods=["GET", "POST"])
@login_required
def department_delete(id):
    """
    If user is admin, renders template to delete department!
    """
    check_admin()
    
    department = Department.query.get_or_404(id)
    
    try:
        db.session.delete(department)
        db.session.commit()
        flash("Department Deleted!")

    except:
        db.session.rollback()
        flash("Department Deletion failed!")
    
    return redirect(url_for("admin.department_list"))


@admin.route("/roles")
@login_required
def role_list():
    """
    If user is admin renders roles/roles.html template!
    """
    check_admin()

    roles = Role.query.all()

    return render_template("admin/roles/roles.html", roles = roles, title="Roles")


@admin.route("/roles/add", methods=["GET", "POST"])
@login_required
def role_add():
    """
    If user is admin render roles/role.html template!
    """
    check_admin()
    add_role = True
    form = RoleForm()

    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)

        try:
            db.session.add(role)
            db.session.commit()
            flash("Role Added Sucessfully!")
            return redirect(url_for("admin.role_list"))
        except:
            db.session.rollback()
            flash("Role Addition failed!")

    return render_template("admin/roles/role.html", add_role=add_role, form=form, title="Add Role")


@admin.route("/roles/edit/<int:id>", methods=["GET", "POST"])
@login_required
def role_edit(id):
    """
    If user is admin, render roles/role.html template,
    And allows edit to edit role!
    """
    check_admin()
    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)

    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data

        try:
            db.session.commit()
            flash("Role Edited!")
            return redirect(url_for("admin.role_list"))

        except:
            db.session.rollback()
            flash("Editting Role failed!")

    form.name.data = role.name
    form.description.data = role.description

    return render_template("admin/roles/role.html", add_role=add_role, form=form, role=role, title="Edit Role")

@admin.route("/roles/delete/<int:id>", methods=["GET", "POST"])
@login_required
def role_delete(id):
    """
    If user is admin, deletes the role and redirect!
    """
    check_admin()

    role = Role.query.get_or_404(id)

    try:
        db.session.delete(role)
        db.session.commit()
        flash("Role deleted successfully!")
    
    except:
        db.session.rollback()
        flash("Role deletion Uncessfull!")
    
    return redirect(url_for("admin.role_list"))


@admin.route("/employees")
@login_required
def employee_list():
    """
    If user is admin, returns the list of all the employees!
    """

    check_admin()

    employees = Employee.query.all()

    return render_template("admin/employees/employees.html", employees = employees, title="Employees")

@admin.route("/employees/assign/<int:id>", methods=["GET", "POST"])
@login_required
def employee_assign(id):
    """
    If user is admin, gives it access to assign department and roles to the employees!
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    if employee.is_admin:
        flash("Employee is Admin!")
        return redirect(url_for("admin.employee_list"))
    
    form = EmployeeAsignForm(obj=employee)

    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data

        try:
            db.session.add(employee)
            db.session.commit()
            flash("Succesfully assigned Department and Role!")

        except:
            db.session.rollback()
            flash("Failed to assign Department and Role")

        return redirect(url_for("admin.employee_list"))

    return render_template("admin/employees/employee.html", form=form, employee=employee, tittle="Assign Employee")