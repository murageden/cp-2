import unittest
from we_connect.review import Review
from we_connect.user import User
from we_connect.business import Business


class reviewTestCase(unittest.TestCase):
    def setUp(self):
        self.review = Review()
        self.user = User()
        self.test_user = self.user.add_user(
            'Test User', 'test@user.com', 'test_user', '1234pass')
        self.business = Business()
        self.test_bs = self.business.add_business(
            'Test Business1', 'Supermarket',
            'Behind Equity Bank',
            'Githurai, Nairobi Area', self.test_user['username'])

    def test_create_review(self):
        self.response = self.review.add_review(
            4, "Nice place for holidays",
            self.test_user['username'], self.test_bs['id'])
        self.assertIn(self.response, Review.reviews)

    def test_returns_all_reviews_for_business(self):
        self.review.add_review(
            4, "Nice place for holidays",
            self.test_user['username'], self.test_bs['id'])
        self.review.add_review(
            1, "Chefs are rude",
            self.test_user['username'], self.test_bs['id'])
        self.assertTrue(len(self.review.view_reviews_for(
            self.test_bs['id'])) == 2)
