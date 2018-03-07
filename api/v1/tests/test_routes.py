import unittest
import jwt

from flask import jsonify, json
from we_connect.routes import app
from we_connect.user import User
from we_connect.business import Business


class EndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.test_user = {
                "name": "Test Name",
                "email": "test@test1.com",
                "username": "test1",
                "password": "1234usr"
            }

        self.test_login = {
                "username": "test1",
                "password": "1234usr"
        }

        self.test_bad_login = {
                "username": "test2",
                "password": "5678usr"
        }

        self.test_business = {
                "name": "Test Biz",
                "category": "shop",
                "description": "The best prices in town",
                "location": "TRM"
        }

        self.test_bs_without_auth = {
                "name": "Test Bad",
                "category": "supermarket",
                "description": "The way to shop",
                "location": "Along Thika Road"
        }

    def test_create_user_endpoint(self):
        self.response = self.client.post('/weconnect/api/v1/auth/register',

                    data=json.dumps(self.test_user),

                    headers={'content-type': 'application/json'})

        self.assertEqual(self.response.status_code, 201)
        self.assertIn("Test Name", str(self.response.data))

    def test_login_user_endpoint(self):
        self.response = self.client.post('/weconnect/api/v1/auth/login',

                    data=json.dumps(self.test_login),

                    headers={'content-type': 'application/json'})

        self.j_response = json.loads(self.response.data)

        data = jwt.decode(self.j_response['token'], app.config['SECRET_KEY'])

        user = User.view_user(data['username'])

        self.assertTrue(self.response.status_code == 201)

        self.assertEqual(user['email'], self.test_user['email'])

    def test_bad_login_returns_a_msg(self):
        self.response = self.client.post('/weconnect/api/v1/auth/login',

                    data=json.dumps(self.test_bad_login),

                    headers={'content-type': 'application/json'})

        self.j_response = json.loads(self.response.data)

        self.assertTrue(self.response.status_code == 400)

        self.assertIn('Wrong', self.j_response['msg'])

    def test_register_business(self):
        self.response = self.client.post('/weconnect/api/v1/auth/login',

                    data=json.dumps(self.test_login),

                    headers={'content-type': 'application/json'})

        self.j_response = json.loads(self.response.data)

        self.response = self.client.post('/weconnect/api/v1/businesses',

                    data=json.dumps(self.test_business),

                    headers={'content-type': 'application/json',
                    'x-access-token': self.j_response['token']})

        self.j_response = json.loads(self.response.data)

        self.assertTrue(self.response.status_code == 201)

        self.assertIn(self.j_response, Business.businesses)

    def test_register_business_with_no_token_returns_error(self):
        self.response = self.client.post('/weconnect/api/v1/businesses',

                    data=json.dumps(self.test_business),

                    headers={'content-type': 'application/json'})

        self.j_response = json.loads(self.response.data)

        self.assertTrue(self.response.status_code == 401)

        self.assertIn('Token is missing', self.j_response['msg'])

        self.assertNotIn(self.j_response, Business.businesses)
