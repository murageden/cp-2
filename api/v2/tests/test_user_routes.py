"""Contain tests for the endpoints."""
from flask import json
import jwt
import unittest
# local imports
from run import db
from we_connect.routes import app


class UserRoutesTestCase(unittest.TestCase):
    """This class represents the routes test case."""

    def setUp(self):
        """Define test variables."""
        self.app = app
        self.client = self.app.test_client()
        self.test_user = {
            "name": "My Test Name",
            "email": "test1@testing.com",
            "username": "test1",
            "password": "1234user"
        }
        self.test_user2 = {
            "name": "My Second Test",
            "email": "test1@testing.com",  # similar email to the previous user
            "username": "test2",
            "password": "1234user"
        }
        self.test_user3 = {
            "name": "My Third Test",
            "email": "test3@testing.com",
            "username": "test1",  # similar username to a previous user
            "password": "1234user"
        }
        self.test_login = {
            "username": "test1",
            "password": "1234user"
        }
        self.test_wrong_pass = {
            "username": "test1",
            "password": "1234users"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_register_user_with_correct_data(self):
        """Test user registration with all info provided."""
        self.response = self.client.post('/weconnect/api/v2/auth/register',
                                         data=json.dumps(self.test_user),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("My Test Name", str(self.response.data))

    def test_register_user_with_existing_email_returns_error_msg(self):
        """Test user registration with all info provided."""
        """Provide a registered email."""
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.test_user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/register',
                                         data=json.dumps(self.test_user2),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.assertEqual(self.response.status_code, 400)
        self.assertIn("already registered!", str(self.response.data))

    def test_register_user_with_registered_username_returns_error_msg(self):
        """Test user registration with all info provided."""
        """Provide a registered username."""
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.test_user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/register',
                                         data=json.dumps(self.test_user3),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.assertEqual(self.response.status_code, 400)
        self.assertIn("not available!", str(self.response.data))

    def test_login_user_with_correct_login(self):
        """Test user login with all log in details provided."""
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.test_user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.assertEqual(self.response.status_code, 200)
        self.assertIn("Log in successful", str(self.response.data))

    def test_login_user_with_non_existent_email(self):
        """Try to login with no user created."""
        """The email is not existing in the data structure."""
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.assertEqual(self.response.status_code, 400)
        self.assertIn("Email or username is incorrect",
                      str(self.response.data))

    def test_login_with_incorrect_email(self):
        """Test user login with all log in details provided."""
        """The password provided is incorrect."""
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.test_user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.test_wrong_pass),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.assertEqual(self.response.status_code, 400)
        self.assertIn("Wrong", str(self.response.data))

    def tearDown(self):
        """Tear down all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
