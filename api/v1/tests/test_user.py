import unittest
from we_connect.user import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_create_user(self):
        self.response = self.user.add_user(
            'Test User', 'test@user.com', 'test_user', '1234pass')

        self.assertIn(self.response, User.users)
