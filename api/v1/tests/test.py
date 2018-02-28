import unittest

from we_connect.user import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_create_user(self):
        self.response = self.user.create_user('Test User', 'test@user.com', '1234pass')
        self.assertEqual(self.response['msg'], 'User id {} created successfully'.format(self.response['id']))