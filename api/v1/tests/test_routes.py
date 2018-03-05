import unittest
from we_connect.routes import app
from we_connect.user import User
from we_connect.business import Business
from we_connect.review import Review


class EndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user = User()
        self.business = Business()
        self.review = Review()

    def test_create_user_endpoint_returns_a_msg(self):
        pass

