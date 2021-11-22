from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Employee(UserMixin, db.Model):
    """
    Employee table defination!
    """
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_encrypt = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    role_id = db.Column(db.Interger, db.Forerignkey("roles.id"))
    is_admin = db.Column(db.boolean, default=False)

    @property
    def password(self):
        """
        Constrain to acces password directly!
        """
        raise AttributeError("Password is not readable!")

    @password.setter
    def password(self, password):
        """
        Sets password in encrypted form!
        """
        self.password_encrypt = generate_passeord_hash(password)

    def verify_password(self, password):
        """
        Check if the encrypted password maches the actual password!
        """
        return check_password_hash(self.password_encrypt, password)
    
    def __repr__(self):
        return "Employee: {}".format(self.username)

@login_manger.user_loader
def load_user(user_id):
    return Employee.query.get(id = int(user_id))

class Department(db.Model):
    """
    Department table defination!
    """
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employess = db.relationshp("Employee", backref="department", lazy="dynamic")

    def __repr__(self):
        return "Department: {}".format(self.name)

class Role(db.Model):
    """
    Roles table defination!
    """
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employess = db.relationshp("Employee", backref="role", lazy="dynamic")

    def __repr__(self):
        return "Role: {}".format(self.name)