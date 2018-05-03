import unittest
import jwt
from flask import jsonify, json
# local imports
from api import app
from api.user import User


class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # initialize app client and test variables
        self.client = app.test_client()
        # complete info to create a user
        self.test_user = {
            "name": "Mark Maroiko",
            "email": "maroikomark@test1.com",
            "username": "mar44",
            "password": "2$4pass"
        }
        # lacks email of the user
        self.incomplete_user = {
            "name": "Mark Maroiko",
            "email": "maroikomark@test1.com",
            "password": "2$4pass"
        }
        # complete login info
        self.test_login = {
            "username": "mar44",
            "password": "2$4pass"
        }
        # wrong combination
        self.test_bad_login = {
            "username": "mar44",
            "password": "5678usr"
        }
        self.test_reset_pass = {
            "old password": "2$4pass",
            "new password": "1$4pack"
        }

    def tearDown(self):
        """Runs after every test"""
        User.users.clear()

    def test_register_a_user(self):
        """Registering a user with all the required info"""
        self.response = self.client.post('/api/v1/auth/register',
                                         data=json.dumps(self.test_user),
                                         headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("Mark Maroiko", str(self.response.data))

    def test_register_a_user_with_missing_details(self):
        """Registering a user with some info missing"""
        self.response = self.client.post('/api/v1/auth/register',
                                         data=json.dumps(self.incomplete_user),
                                         headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 400)
        self.assertNotIn("Test Name", str(self.response.data))
        self.assertIn("Please provide username", str(self.response.data))

    def test_login_a_user(self):
        """Log in a user with correct user credentials"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        data = jwt.decode(self.token, app.config['SECRET_KEY'])
        user = User.view_user(data['username'])
        self.assertTrue(self.response.status_code == 200)
        self.assertEqual(user['email'], self.test_user['email'])

    def test_login_user_with_incorrect_credentials(self):
        """Try to log in a user using wrong credentials"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_bad_login),
                                         headers={'content-type': 'application/json'})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 400)
        self.assertIn('Wrong', self.j_response['msg'])

    def test_login_an_already_logged_in_user(self):
        """Try to log in a user twice"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.client.post('/api/v1/auth/login',
                         data=json.dumps(self.test_login),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.assertTrue(self.response.status_code == 400)
        self.assertIn("User already logged in", str(self.response.data))

    def test_logout_a_user(self):
        """Logging out a user"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.log_resp = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.log_resp.data)['token']
        self.response = self.client.post('/api/v1/auth/logout',
                                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.assertTrue(self.response.status_code, 200)
        self.assertIn("User log out successfull", str(self.response.data))

    def test_log_out_already_logged_out_user(self):
        """Try to log out a user twice"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.log_resp = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.log_resp.data)['token']
        self.client.post('/api/v1/auth/logout',
                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.response = self.client.post('/api/v1/auth/logout',
                                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.assertTrue(self.response.status_code, 200)
        self.assertIn("User already logged out", str(self.response.data))

    def test_reset_user_password(self):
        """Tests for reseting a user password functionality"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.log_resp = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.log_resp.data)['token']
        self.response = self.client.post('/api/v1/auth/reset-password',
                                         data=json.dumps(
                                             self.test_reset_pass),
                                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.assertTrue(self.response.status_code, 200)
        self.assertIn("Password changed successfully", str(self.response.data))
