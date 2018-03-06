import unittest
from we_connect.business import Business


class BusinessTestCase(unittest.TestCase):
    def setUp(self):
        self.business = Business()


    def test_add_business(self):
        self.response = self.business.add_business(
            'Test Business1', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.assertIn(self.response['business'], Business.businesses)

    def test_returns_a_business_if_business_exists(self):
        self.response_add = self.business.add_business(
            'Test Business2', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_read = self.business.view_business(
            self.response_add['business']['id'])
        self.assertIn(self.response_read, Business.businesses)


    def test_updates_a_business_exists(self):
        self.response = self.business.add_business(
            'Test Business3', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)

        self.business.update_business(
            self.response['business']['id'],
            'Modify Business', 'Shop',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)

        self.new_business = self.business.view_business(
            self.response['business']['id'])

        self.assertFalse(self.new_business['name'] == 'Test Business3')

        self.assertIn(self.new_business, Business.businesses)


    def test_deletes_a_business_if_exists(self):
        self.response = self.business.add_business(
            'Test Business5', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)

        self.business.delete_business(
            self.response['business']['id'])

        self.assertFalse(self.business.view_business(
            self.response['business']['id']))

        self.assertNotIn(self.business.view_business(
            self.response['business']['id']), Business.businesses)
