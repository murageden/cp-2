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
            "name": "Test Business",
            "description": "The best place to shop",
            "category": "supermarket",
            "location": "Nairobi"
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
    
    ## tests for business endpoints
    def test_register_business_endpoint(self):
        response = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Test Business", str(response.data))

    def test_register_buiness_when_not_logged_in_returns_msg(self):
        response_logout = self.client.post('/weconnect/api/v1/auth/logout',
                    data=json.dumps({}),
                    headers={'content-type': 'application/json'})
        response_reg = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        self.assertIn("You must log in first", str(response_reg.data))

    def test_update_business_endpoint(self):
        response_login = self.client.post('/weconnect/api/v1/auth/login',
        data=json.dumps(self.test_login),
        headers={'content-type': 'application/json'})
        response_update = self.client.post(
            f'/weconnect/api/v1/businesses/1',
                    data=json.dumps(self.new_business),
                    headers={'content-type': 'application/json'})