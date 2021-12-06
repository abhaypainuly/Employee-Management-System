import unittest
from flask_testing import TestCase

from flask import url_for, abort

from app import create_app, db
from app.models import Employee, Department, Role


class TestBase(TestCase):

    def create_app(self):
        """
        Will create the application!
        """
        app = create_app()       

        return app

    def setUp(self):
        """
        Will be called before every test!
        """
        # Creating database
        db.create_all()

        # Creating admin
        admin = Employee(username="admin", password="admin@123", is_admin=True)

        # Creating a user
        employee = Employee(username="test_user", password="test@123")

        # Commiting to the database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test case!
        """
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    """
    Class to test all the models!
    """

    def test_employee_model(self):
        """
        Test number of records in Employee table!
        """
        # Adding the another test user
        employee = Employee(username="test_user1", password="test1@123")
        db.session.add(employee)

        self.assertEqual(Employee.query.count(), 3)
    
    def test_department_model(self):
        """
        Test number of records in Departmnet table!
        """
        # Create Departments
        department1 = Department(name="Computer Science", description="The Computer Science Department!")
        department2 = Department(name="Electrical Engineer", description="The Electrical Engineer Department!")

        # Adding departments to the database
        db.session.add(department1)
        db.session.add(department2)
        db.session.commit()

        self.assertEqual(Department.query.count(), 2)

    def test_role_model(self):
        """
        Test number of records in the Role table!
        """
        # Creating roles
        role1 = Role(name="Employee", description="Person working in the department!")
        role2 = Role(name="Manager", description="Person managing a small team under him!")
        role3 = Role(name="Vice President", description="Person manger a devision of the company!")
        
        # Adding roles to the database
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.commit()

        self.assertEqual(Role.query.count(), 3)


class TestViews(TestBase):
    """
    Class to test views!
    """
    def test_homepage_view(self):
        """
        Testing if homepage is accessible without login!
        """
        response = self.client.get(url_for("home.homepage"))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Testing if loginpage is accessible without login!
        """
        response = self.client.get(url_for("auth.login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Testing if logout link is inaccessible without login
        And redirects to login page!
        """
        target_url = url_for("auth.logout")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def test_dashboard_view(self):
        """
        Testing if accessing dashboards without login
        redirects it to login page or not!
        """
        target_url = url_for("home.dashboard")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_admin(self):
        """
        Testing that admin dashboard is not
        accessible without login! 
        """
        target_url = url_for("home.admin_dashboard")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_departments_view(self):
        """
        Test that departments page is inaccessible without login
        and redirects to login page then to departments page!
        """
        target_url = url_for('admin.department_list')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page!
        """
        target_url = url_for('admin.role_list')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_employees_view(self):
        """
        Test that employees page is inaccessible without login
        and redirects to login page then to employees page!
        """
        target_url = url_for('admin.employee_list')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data.decode())

    def test_404_not_found(self):
        response = self.client.get('/random_url')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data.decode())

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data.decode())

if __name__ == "__main__":
    unittest.main()