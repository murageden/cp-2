import unittest
from api.businesses import Business
from api.users import User


class BusinessTestCase(unittest.TestCase):
    def setUp(self):
        self.business = Business()
        self.user = User()
        self.test_user = self.user.add_user(
            'Test User', 'test@user.com', 'test_user', '2$4pass')

    def test_add_business(self):
        self.response = self.business.add_business(
            'Test Business1', 'Supermarket',
            'Behind Equity Bank',
            'Githurai, Nairobi Area', self.test_user['username'])
        self.assertIn(self.response, Business.businesses)

    def test_returns_a_business_if_business_exists(self):
        self.response_add = self.business.add_business(
            'Test Business2', 'Supermarket',
            'Behind Equity Bank',
            'Githurai, Nairobi Area', self.test_user['username'])
        self.response_read = self.business.view_business(
            self.response_add['id'])
        self.assertIn(self.response_read, Business.businesses)

    def test_updates_a_business__if_exists(self):
        self.response = self.business.add_business(
            'Test Business3', 'Supermarket',
            'Behind Equity Bank',
            'Githurai, Nairobi Area', self.test_user['username'])
        self.business.update_business(
            self.response['id'],
            'Modify Business', 'Shop',
            'Behind Equity Bank', 'Eldoret')
        self.new_business = self.business.view_business(
            self.response['id'])
        self.assertFalse(self.new_business['name'] == 'Test Business3')
        self.assertIn(self.new_business, Business.businesses)

    def test_deletes_a_business_if_exists(self):
        self.response = self.business.add_business(
            'Test Business4', 'Shop',
            'Best Prices', 'Mombasa', self.test_user['username'])
        self.business.delete_business(
            self.response['id'])
        self.assertFalse(self.business.view_business(
            self.response['id']))
        self.assertNotIn(self.business.view_business(
            self.response['id']), Business.businesses)

    def test_search_business_by_location(self):
        self.response = self.business.search_business_by_location(
            'Githurai, Nairobi Area')
        self.assertTrue(len(self.response) == 2)

    def test_search_business_by_category(self):
        self.response = self.business.search_business_by_category(
            'Supermarket')
        self.assertTrue(len(self.response) == 2)