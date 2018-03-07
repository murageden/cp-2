import unittest
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

    def test_create_user_endpoint(self):
        self.response = self.client.post('/weconnect/api/v1/auth/register',

                    data=json.dumps(self.test_user),

                    headers={'content-type': 'application/json'})

        self.assertEqual(self.response.status_code, 201)
        self.assertIn("Test Name", str(self.response.data))
