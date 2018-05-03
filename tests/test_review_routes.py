import unittest
from flask import jsonify, json

# local imports
from api import app
from api.review import Review
from api.user import User
from api.business import Business


class ReviewRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # initialize app client and test variables
        self.client = app.test_client()
        # complete data to create a review
        self.test_review = {
            "rating": 4,
            "body": "Good place for holidays"
        }
        # incomplete data to create a review
        self.wrong_review = {
            "rating": "4",
            "body": "Good place for holidays"
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
        # complete info to create a user
        self.another_user = {
            "name": "Peter Marangi",
            "email": "pmarangi@gmail.com",
            "username": "marangip",
            "password": "2$4pass"
        }
        # complete login info
        self.another_login = {
            "username": "marangip",
            "password": "2$4pass"
        }
        # complete business info
        self.test_business = {
            "name": "bsna Poa",
            "category": "shop",
            "description": "The best prices in town",
            "location": "Near TRM"
        }
        # complete business info
        self.another_business = {
            "name": "bsna Ingine",
            "category": "supermarket",
            "description": "Better value, better prices",
            "location": "Along Thika Super Highway"
        }

    def tearDown(self):
        User.users.clear()
        Business.businesses.clear()
        Review.reviews.clear()

    def test_create_review_with_complete_data_and_token(self):
        """Creating a review passing the correct data and token"""
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.test_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.test_login),
                                         headers={'content-type': 'application/json'})
        self.token1 = json.loads(self.response.data)['token']
        self.client.post('/api/v1/businesses',
                         data=json.dumps(self.test_business),
                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token1})
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.another_user),
                         headers={'content-type': 'application/json'})
        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps(self.another_login),
                                         headers={'content-type': 'application/json'})
        self.token2 = json.loads(self.response.data)['token']
        self.client.post('/api/v1/businesses',
                         data=json.dumps(self.test_business),
                         headers={'content-type': 'application/json',
                                                  'x-access-token': self.token2})
        self.response = self.client.post(
            '/api/v1/businesses/2/reviews',
            data=json.dumps(self.test_review),
            headers={'content-type': 'application/json',
                     'x-access-token': self.token1})
        self.assertEqual(self.response.status_code, 201)
        self.j_response = json.loads(self.response.data)

    def test_create_review_with_invalid_token(self):
        """Try to create a review without passing a token"""
        self.response = self.client.post(
            '/api/v1/businesses/1/reviews',
            data=json.dumps(self.test_review),
            headers={'content-type': 'application/json',
                     'x-access-token': 'nonthing here'})
        self.assertEqual(self.response.status_code, 401)
        self.assertIn("Token is invalid", str(self.response.data))

    def test_create_review_with_non_value_ratings(self):
        """Try to create a review with non value ratings"""
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
        self.response = self.client.post(
            f'/api/v1/businesses/{self.js_resp["details"]["id"]}/reviews',
            data=json.dumps(self.wrong_review),
            headers={'content-type': 'application/json',
                     'x-access-token': self.token})
        self.assertEqual(self.response.status_code, 400)
        self.j_response = json.loads(self.response.data)
        self.assertNotIn(self.j_response, Review.reviews)
        self.assertIn("Ratings must be values", str(self.j_response))
