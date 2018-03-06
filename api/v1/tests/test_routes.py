import unittest
import json

from flask import jsonify
from we_connect.routes import app
from we_connect.user import User
from we_connect.business import Business


class EndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        ## test data for a test user
        self.test_user = {
            "name": "Test User",
            'username': 'test_user',
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

        ## test data for a test business
        self.test_business = {
            "name": "Test Business",
            "description": "The best place to shop",
            "category": "supermarket",
            "location": "Nairobi"
        }
        self.new_business = {
            "name": "New Business",
            "description": "The best place to shop",
            "category": "shop",
            "location": "Nairobi"
        }

    def test_create_user_endpoint(self):
        self.response = self.client.post('/weconnect/api/v1/auth/register',
                    data=json.dumps(self.test_user),
                    headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("Test User", str(self.response.data))

    def test_login_user_endpoint(self):
        self.response = self.client.post('/weconnect/api/v1/auth/login',
        data=json.dumps(self.test_login),
        headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 201)

    def test_bad_login_returns_error_msg(self):
        self.response = self.client.post('/weconnect/api/v1/auth/login',
        data=json.dumps(self.test_login),
        headers={'content-type': 'application/json'})
        self.assertIn("Wrong", str(self.response.data))

    # tests for business endpoints

    def test_register_business_endpoint(self):
        self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.response = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 200)
        self.assertIn("Test Business", str(self.response.data))

    # Also aplies to registration of a business when not logged in
    def test_register_business_when_not_logged_in_returns_msg(self):
        self.client.post('/weconnect/api/v1/auth/logout',
                    data=json.dumps({}),
                    headers={'content-type': 'application/json'})
        self.response = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        self.assertIn("You must log in first", str(self.response.data))

    def test_update_business_endpoint(self):
        self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        response = self.client.put('/weconnect/api/v1/businesses/1',
                    data=json.dumps(self.new_business),
                    headers={'content-type': 'application/json'})
        self.assertIn("New Business", str(response.data))

    def test_update_business_returns_error_if_business_not_exists(self):
        self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        response = self.client.put('/weconnect/api/v1/businesses/1000',
                    data=json.dumps(self.new_business),
                   headers={'content-type': 'application/json'})
        self.assertIn("not found", str(response.data))

    def test_deletes_business_if_exists(self):
        self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        response = self.client.delete('/weconnect/api/v1/businesses/1',
                    data=json.dumps(self.new_business),
                    headers={'content-type': 'application/json'})
        self.assertIn("deleted", str(response.data))

        