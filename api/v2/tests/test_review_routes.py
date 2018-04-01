"""Contain tests for the user endpoints."""
from flask import json
import unittest
# local imports
from run import db
from we_connect.routes import app


class ReviewRoutesTestCase(unittest.TestCase):
    """This class represents the review routes test case."""

    def setUp(self):
        """Define test variables."""
        self.app = app
        self.client = self.app.test_client()
        # for registering a review
        self.test_review = {
            "rating": 4,
            "body": "Good place for holidays"
        }
        # for registering a review containing invalid data
        self.wrong_review = {
            "rating": "4",
            "body": "Good place for holidays"
        }
        # for registering a user
        self.user = {
            "name": "My Test Name",
            "email": "test1@testing.com",
            "username": "test1",
            "password": "1234user"
        }
        # for registering a user
        self.another_user = {
            "name": "Another Test Name",
            "email": "test2@testing.com",
            "username": "test2",
            "password": "5678user"
        }
        # for logging in a user
        self.login = {
            "username": "test1",
            "password": "1234user"
        }
        # for logging in a user
        self.another_login = {
            "username": "test2",
            "password": "5678user"
        }
        # for registering a bs
        self.bs = {
            "name": "Test Business",
            "category": "shop",
            "description": "The best prices in town",
            "location": "Near TRM"
        }
        # for registering a bs
        self.another_bs = {
            "name": "Test Business",
            "category": "shop",
            "description": "Holiday shopping ongoing, enjoy discounts",
            "location": "Near TRM"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_review_for_an_existing_business(self):
        """Test creation of a review with all required details."""
        """Register two users, each businesses, create review for one."""
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.login),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.token = json.loads(self.response.data)['token']  # grab the token
        self.client.post('/weconnect/api/v2/businesses',
                         data=json.dumps(self.bs),
                         headers={
                             'content-type': 'application/json',
                             'x-access-token': self.token
                         })
        # Register another user, login them and register their business
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.another_user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.another_login),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.token = json.loads(self.response.data)['token']  # grab the token
        self.client.post('/weconnect/api/v2/businesses',
                         data=json.dumps(self.another_bs),
                         headers={
                             'content-type': 'application/json',
                             'x-access-token': self.token
                         })
        # this user reviews bs 1 which belongs to the other user
        self.response = self.client.post('/weconnect/api/v2/businesses/1/reviews',
                                         data=json.dumps(self.test_review),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token
                                         })
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("Good place for holidays",
                      str(self.response.data))

    def test_create_review_for_own_business(self):
        """Try to create a review for a business owned by the current user."""
        """Register a user, login, grab token, register business"""
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.login),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.token = json.loads(self.response.data)['token']  # grab the token
        self.client.post('/weconnect/api/v2/businesses',
                         data=json.dumps(self.bs),
                         headers={
                             'content-type': 'application/json',
                             'x-access-token': self.token
                         })
        self.response = self.client.post('/weconnect/api/v2/businesses/1/reviews',
                                         data=json.dumps(self.test_review),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.token
                                         })
        self.assertEqual(self.response.status_code, 400)
        self.assertIn("This business belongs to you",
                      str(self.response.data))

    def test_retrieves_all_reviews_for_a_business(self):
        """Create two reviews for a business, try to get them."""
        """Register two users, each businesses, create reviews for one."""
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.login),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.token = json.loads(self.response.data)['token']  # grab the token
        self.client.post('/weconnect/api/v2/businesses',
                         data=json.dumps(self.bs),
                         headers={
                             'content-type': 'application/json',
                             'x-access-token': self.token
                         })
        # Register another user, login them and register their business
        self.client.post('/weconnect/api/v2/auth/register',
                         data=json.dumps(self.another_user),
                         headers={
                             'content-type': 'application/json'
                         })
        self.response = self.client.post('/weconnect/api/v2/auth/login',
                                         data=json.dumps(self.another_login),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.token = json.loads(self.response.data)['token']  # grab the token
        self.client.post('/weconnect/api/v2/businesses',
                         data=json.dumps(self.another_bs),
                         headers={
                             'content-type': 'application/json',
                             'x-access-token': self.token
                         })
        # this user reviews bs 1 which belongs to the other user
        self.client.post('/weconnect/api/v2/businesses/1/reviews',
                         data=json.dumps(self.test_review),
                         headers={
                             'content-type': 'application/json',
                             'x-access-token': self.token
                         })
        self.client.post('/weconnect/api/v2/businesses/1/reviews',
                         data=json.dumps(self.test_review),
                         headers={
                             'content-type': 'application/json',
                             'x-access-token': self.token
                         })
        self.response = self.client.get('/weconnect/api/v2/businesses/1/reviews')
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(len(json.loads(self.response.data)['reviews']), 2)

    def tearDown(self):
        """Tear down all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
