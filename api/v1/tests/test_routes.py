import unittest
import json

from flask import jsonify
from we_connect.routes import app
from we_connect.user import User


class EndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.test_user = {
            "name": "Test User",
            "email": "test@user.com",
            "password": "1234pass"
        }
        self.test_login = {
            "email": "test@user.com",
            "password": "1234pass"
        }
        self.bad_login = {
            "email": "bad@bad.com",
            "password": "1234notpass"
        }

    def test_create_user_endpoint(self):
        response = self.client.post('/weconnect/api/v1/auth/register',
                    data=json.dumps(self.test_user),
                    headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Test User", str(response.data))

    def test_login_user_endpoint(self):
        response = self.client.post('/weconnect/api/v1/auth/login',
        data=json.dumps(self.test_login),
        headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.test_user['email'], User.user_logged_in['email'])

    def test_bad_login_returns_error_msg(self):
        response = self.client.post('/weconnect/api/v1/auth/login',
        data=json.dumps(self.test_login),
        headers={'content-type': 'application/json'})
        self.assertIn("Wrong", str(response.data))