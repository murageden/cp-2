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
            'Test Business1', 'Supermarket', 'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.assertEqual(self.response['msg'],
        'Business id {} created successfully'.format(
            self.response['id']))
    def test_returns_a_business_if_business_exists(self):
        self.response_add = self.business.create_business(
            'Test Business2', 'Supermarket', 'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_read = self.business.view_business(
            self.response_add['id'])
        self.assertEqual(self.response_read['msg'], 'okay')

    # This applies for updating, deleting, viewing
    # a non-existing business
    def test_returns_a_message_if_business_does_not_exist(self):
        self.response = self.business.view_business(1000)
        self.assertEqual(
            self.response['msg'], 'Business id {} not found'.format(
                self.response['id']))

    def test_updates_a_business_for_owner_if_business_exists(self):
        self.response_add = self.business.create_business(
            'Test Business3', 'Supermarket', 'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_modify = self.business.update_business(
            self.response_add['id'], 'Modify Business', 'Shop', 'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.assertEqual(
            self.response_modify['msg'], 'Business id {} modified successfully'.format(
                self.response_modify['id']))

    def test_returns_error_if_updater_is_not_owner(self):
        self.response_add = self.business.create_business(
            'Test Business4', 'Supermarket', 'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_modify = self.business.update_business(
            self.response_add['id'], 'Modify Business', 'Shop', 'Behind Equity Bank', 'Githurai, Nairobi Area', 5)
        self.assertEqual(
            self.response_modify['msg'], 'You cannot update this business')

    def test_deletes_a_business_if_exists(self):
        self.response_add = self.business.create_business(
            'Test Business5', 'Supermarket', 'Behind Equity Bank', 'Githurai, Nairobi Area', 4)
        self.response_delete = self.business.delete_business(
            self.response_add['id'])
        self.assertEqual(
            self.response_delete['msg'], 'Business id {} deleted successfully'.format(
            self.response_delete['id']))