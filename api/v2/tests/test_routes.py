"""Contain tests for the endpoints."""
from flask import jsonify, json
import jwt
import unittest
# local imports
from we_connect import db
from we_connect.routes import app


class RoutesTestCase(unittest.TestCase):
    """This class represents the routes test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client()
        self.test_user = {
            "name": "My Test Name",
            "email": "test1@testing.com",
            "username": "test0",
            "password": "1234user"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_register_user_with_correct_data(self):
        """Test user registration with all info provided."""
        self.response = self.client.post('/weconnect/api/v2/auth/register',
                                         data=json.dumps(self.test_user),
                                         headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("My Test Name", str(self.response.data))

    def tearDown(self):
        """Teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
