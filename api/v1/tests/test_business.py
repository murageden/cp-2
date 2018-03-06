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

    # This applies for updating, deleting, viewing
    # a non-existing business
    def test_returns_a_message_if_business_does_not_exist(self):
        self.response = self.business.view_business(1000)
        # Check that response is not a business object
        self.assertNotIn(self.response, Business.businesses)
        self.assertEqual(
            self.response['msg'],
            f'Business id {self.response["id"]} not found')

    def test_updates_a_business_for_owner_if_business_exists(self):
        self.response_add = self.business.add_business(
            'Test Business3', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_modify = self.business.update_business(
            self.response_add['business']['id'],
            'Modify Business', 'Shop',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.updated_business = self.business.view_business(
            self.response_modify['id'])
        self.assertIn(self.updated_business, Business.businesses)
        self.assertEqual(self.response_modify['msg'],
            f'Business id {self.response_modify["id"]} modified successfully')

    def test_returns_error_if_updater_is_not_owner(self):
        self.response_add = self.business.add_business(
            'Test Business4', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_modify = self.business.update_business(
            self.response_add['business']['id'],
            'Modify Business', 'Shop',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 5)
        self.assertEqual(
            self.response_modify['msg'], 'You cannot update this business')

    def test_deletes_a_business_if_exists(self):
        self.response_add = self.business.add_business(
            'Test Business5', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_delete = self.business.delete_business(
            self.response_add['business']['id'])
        self.response_view = self.business.view_business(
            self.response_delete['id'])
        self.assertEqual(
            self.response_view['msg'],
            f'Business id {self.response_view["id"]} not found')
        self.assertEqual(self.response_delete['msg'],
            f'Business id {self.response_delete["id"]} deleted successfully')
