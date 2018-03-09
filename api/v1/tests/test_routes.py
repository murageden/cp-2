import unittest
import jwt

from flask import jsonify, json
from we_connect.routes import app
from we_connect.user import User
from we_connect.business import Business
from we_connect.review import Review


class EndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.test_user = {
                "name": "Test Name",
                "email": "test@test1.com",
                "username": "test1",
                "password": "1234usr"
        }
        # lacks email of the user
        self.incomplete_user = {
                "name": "Test Name",
                "email": "test4@test1.com",
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
        # lacks name of the business
        self.incomplete_bs = {
                "category": "shop",
                "description": "The best prices in town",
                "location": "TRM"
        }

        self.new_business = {
                "name": "Updated Biz",
                "category": "supermarket",
                "description": "The best prices in town",
                "location": "TRM"
        }

        self.test_review = {
                "rating": 4,
                "body": "Good place for holidays"
        }

        self.wrong_review = {
                "rating": "4",
                "body": "Good place for holidays"
        }

    def test_create_user_without_some_required_data(self):
        """
            Tries to create a user, sending incomplete data
            Expects an error, Resource should not be created
        """
        self.response = self.client.post('/weconnect/api/v1/auth/register',
                    data=json.dumps(self.incomplete_user),
                    headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 400)
        self.assertNotIn("Test Name", str(self.response.data))
        self.assertIn("Missing details", str(self.response.data))

    def test_create_user_with_correct_data(self):
        """
            Creates a user, sending all required data
            Expects success, Resource should be created
        """
        self.response = self.client.post('/weconnect/api/v1/auth/register',
                    data=json.dumps(self.test_user),
                    headers={'content-type': 'application/json'})
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("Test Name", str(self.response.data))

    def test_login_user_with_correct_data(self):
        """
            Logs in a user, sending all required data
            Expects success, success message expected
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        data = jwt.decode(self.token, app.config['SECRET_KEY'])
        user = User.view_user(data['username'])
        self.assertTrue(self.response.status_code == 200)
        self.assertEqual(user['email'], self.test_user['email'])

    def test_bad_login_returns_an_error(self):
        """
            Tries to log in a user, sending incomplete data
            Expects an error
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_bad_login),
                    headers={'content-type': 'application/json'})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 400)
        self.assertIn('Wrong', self.j_response['msg'])

    def test_register_business_with_correct_data_and_token(self):
        """
            Registers a business, sending all required data
            Including the authentication token
            Expects success, success message expected
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.response = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 201)
        self.assertIn(self.j_response, Business.businesses)

    def test_register_business_without_token(self):
        """
            Tries to resister a business, sending all required data
            Except the authentication token
            Expects an error
        """
        self.response = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json'})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 401)
        self.assertIn('Token is missing', self.j_response['msg'])
        self.assertNotIn(self.j_response, Business.businesses)

    def test_update_business_with_correct_data_and_token(self):
        """
            Updates a business, sending all required data
            Expects success, success message expected
            Resource should be updated
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.response = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.response = self.client.put(
            f'/weconnect/api/v1/businesses/{self.j_response["id"]}',
                    data=json.dumps(self.new_business),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.assertIn('Updated Biz', str(self.j_response))
        self.assertIn(self.j_response, Business.businesses)

    def test_update_business_with_incorrect_data_and_token(self):
        """
            Tries to update a business, sending incomplete data
            Including the auth token
            Expects success, success message expected
            Resource should be updated
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.response = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.j_response = json.loads(self.response.data)
        self.response = self.client.put(
            f'/weconnect/api/v1/businesses/{self.j_response["id"]}',
                    data=json.dumps(self.incomplete_bs),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.assertEqual(self.response.status_code, 400)
        self.assertIn('Missing details', str(self.response.data))

    def test_update_business_without_token(self):
        """
            Tries to update a business, sending all required data
            Except the auth token
            Expects an error
            Resource should not be updated
        """
        self.response = self.client.put('/weconnect/api/v1/businesses/1',
                    data=json.dumps(self.new_business),
                    headers={'content-type': 'application/json'})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 401)
        self.assertIn('Token is missing', self.j_response['msg'])
        self.assertNotIn(self.j_response, Business.businesses)

    def test_delete_own_business_with_token(self):
        """
            Tries to delete a business, using the auth token
            Expects success, success msg
            Resource should be deleted
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.resp_reg = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.js_resp = json.loads(self.resp_reg.data)
        self.length1 = len(Business.businesses)
        self.response = self.client.delete(
            f'/weconnect/api/v1/businesses/{self.js_resp["id"]}',
                    data=json.dumps({}),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.length2 = len(Business.businesses)
        self.assertTrue(self.length2 < self.length1)
        self.assertTrue(self.response.status_code == 200)
        self.j_response = json.loads(self.response.data)
        self.assertNotIn(self.j_response, Business.businesses)

    def test_delete_business_without_token(self):
        """
            Tries to delete a business, without the auth token
            Expects an error
            Resource should not be deleted
        """
        self.response = self.client.delete('/weconnect/api/v1/businesses/1',
                    data=json.dumps({}),
                    headers={'content-type': 'application/json'})
        self.j_response = json.loads(self.response.data)
        self.assertTrue(self.response.status_code == 401)
        self.assertIn('Token is missing', self.j_response['msg'])

    def test_creates_a_review_for_a_business_with_token_and_correct_data(self):
        """
            Tries to create a review, using the auth token, with correct data
            Expects success, success msg
            Resource should be created
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.resp_reg = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.js_resp = json.loads(self.resp_reg.data)
        self.response = self.client.post(
            f'/weconnect/api/v1/businesses/{self.js_resp["id"]}/reviews',
                    data=json.dumps(self.test_review),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.assertEqual(self.response.status_code, 201)
        self.j_response = json.loads(self.response.data)
        self.assertIn(self.j_response, Review.reviews)

    def test_creates_a_review_for_a_business_with_token_and_incorrect_data(self):
        """
            Tries to create a review, using the auth token, passing incorrect data
            Expects error
            Resource should not be created
        """
        self.response = self.client.post('/weconnect/api/v1/auth/login',
                    data=json.dumps(self.test_login),
                    headers={'content-type': 'application/json'})
        self.token = json.loads(self.response.data)['token']
        self.resp_reg = self.client.post('/weconnect/api/v1/businesses',
                    data=json.dumps(self.test_business),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.js_resp = json.loads(self.resp_reg.data)
        self.response = self.client.post(
            f'/weconnect/api/v1/businesses/{self.js_resp["id"]}/reviews',
                    data=json.dumps(self.wrong_review),
                    headers={'content-type': 'application/json',
                    'x-access-token': self.token})
        self.assertEqual(self.response.status_code, 400)
        self.j_response = json.loads(self.response.data)
        self.assertNotIn(self.j_response, Review.reviews)
        self.assertIn("Ratings must be values", str(self.j_response))

    def test_create_review_for_business_without_token_returns_error(self):
        """
            Tries to create a review for non-existing business
            Without using the auth token
            Expects error
            Resource should not be created
        """
        self.response = self.client.post(
            '/weconnect/api/v1/businesses/1/reviews',
                    data=json.dumps(self.test_review),
                    headers={'content-type': 'application/json',
                    'x-access-token': 'nonthing here'})
        self.assertEqual(self.response.status_code, 401)
        self.assertIn("Token is invalid", str(self.response.data))
