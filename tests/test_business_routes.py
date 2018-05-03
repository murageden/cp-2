import unittest
from flask import jsonify, json
# local imports
from api import app
from api.business import Business
from api.user import User

class BusinessRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # initialize app client and test variables
        self.client = app.test_client()
        # complete business info
        self.test_business = {
            "name": "bsna Poa",
            "category": "shop",
            "description": "The best prices in town",
            "location": "Near TRM"
        }
        # incomplete business info
        self.incomplete_bs = {
            "category": "shop",
            "description": "The best prices in town",
            "location": "TRM"
        }
        # updating a business
        self.update_business = {
            "name": "Updated bsna",
            "category": "supermarket",
            "description": "The best prices in town",
            "location": "TRM"
        }
        # complete info to create a user
        self.test_user = {
            "name": "Mark Maroiko",
            "email": "maroikomark@test1.com",
            "username": "mar44",
            "password": "2$4pass"
        }
        # complete login info
        self.test_login = {
            "username": "mar44",
            "password": "2$4pass"
        }

    def tearDown(self):
        User.users.clear()
        Business.businesses.clear()

    def test_register_business_with_complete_data(self):
        """Registers a business sending all the required info"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.response = self.client.post('/api/v1/businesses',
                                         data=json.dumps(
                                             self.test_business),
                                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 201)

    def test_register_business_without_token(self):
        """Registers a business without sending the required token"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.response = self.client.post('/api/v1/businesses',
                                         data=json.dumps(self.test_business),
                                         headers={'content-type': 'application/json'})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 401)
        self.assertIn('Token is missing', self.j_response['msg'])
        self.assertNotIn(self.j_response, Business.businesses)

    def test_update_business_with_correct_data_and_token(self):
        """Updates a business, sending all required data"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.response = self.client.post('/api/v1/businesses',
                                         data=json.dumps(self.test_business),
                                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.response = self.client.put(
            '/api/v1/businesses/1',
            data=json.dumps(self.update_business),
            headers={'content-type': 'application/json',
                     'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.assertIn('Updated bsna', str(self.j_response))

    def test_update_business_with_incorrect_data_and_token(self):
        """Try to update a business sending all data except token"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.response = self.client.post('/api/v1/businesses',
                                         data=json.dumps(self.test_business),
                                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.response = self.client.put(
            '/api/v1/businesses/1',
            data=json.dumps(self.incomplete_bs),
            headers={'content-type': 'application/json',
                     'x-access-token': self.token})
        self.assertEqual(self.response.status_code, 400)
        self.assertIn('Please provide name', str(self.response.data))

    def test_update_business_without_token(self):
        """Try to update business without sending a token"""
        self.response = self.client.put('/api/v1/businesses/1',
                                        data=json.dumps(self.update_business),
                                        headers={'content-type': 'application/json'})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 401)
        self.assertIn('Token is missing', self.j_response['msg'])
        self.assertNotIn(self.j_response, Business.businesses)

    def test_delete_own_business_with_token(self):
        """Delete an own business sending the token"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.resp_reg = self.client.post('/api/v1/businesses',
                                         data=json.dumps(self.test_business),
                                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token})
        self.js_resp = json.loads(self.resp_reg.data)
        self.response = self.client.delete(
            '/api/v1/businesses/1',
            data=json.dumps({}),
            headers={'content-type': 'application/json',
                     'x-access-token': self.token})
        self.assertTrue(self.response.status_code == 200)
        self.j_response = json.loads(self.response.data)
        self.assertNotIn(self.j_response, Business.businesses)

    def test_delete_business_without_token(self):
        """Try to delete a business without providing the token"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.resp_reg = self.client.post('/api/v1/businesses',
                                         data=json.dumps(self.test_business),
                                         headers={'content-type': 'application/json'})
        self.js_resp = json.loads(self.resp_reg.data)
        self.response = self.client.delete(
            '/api/v1/businesses/1',
            data=json.dumps({}),
            headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 401)
        self.assertIn("Token is missing", str(self.response.data))
