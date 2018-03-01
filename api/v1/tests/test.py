import unittest
from we_connect.user import User
from we_connect.business import Business


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_create_user(self):
        self.response = self.user.create_user(
            'Test User', 'test@user.com', '1234pass')
        self.assertEqual(self.response['msg'],
        'User id {} created successfully'.format(
            self.response['id']))

    def test_get_all_users(self):
        pass

class BusinessTestCase(unittest.TestCase):
    def setUp(self):
        self.business = Business()
    
    def test_create_business(self):
        self.response = self.business.create_business(
            'Test Business', 'Supermarket', 'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.assertEqual(self.response['msg'],
        'Business id {} created successfully'.format(
            self.response['id']))