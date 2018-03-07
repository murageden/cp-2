import unittest
from flask import jsonify, json
from we_connect.routes import app
from we_connect.user import User
from we_connect.business import Business


class EndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_user_endpoint(self):
        self.response = self.client.post('/weconnect/api/v1/auth/register',

                    data=json.dumps(self.test_user),

                    headers={'content-type': 'application/json'}

        self.assertEqual(self.response.status_code, 201)
        self.assertIn("Test User", str(self.response.data))
