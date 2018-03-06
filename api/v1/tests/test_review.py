import unittest
from we_connect.review import Review
from we_connect.user import User
from we_connect.business import Business


class reviewTestCase(unittest.TestCase):
    def setUp(self):
        self.review = Review()
        self.user = User()
        self.business = Business()

    def test_create_review(self):
        # create a user
        self.response_user = self.user.add_user(
            'Test User', 'test@user.com', '1234pass')
        self.userId = self.response_user['user']['id']

        # create a business for this user
        self.response_bs = self.business.add_business(
            'Test Business1', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', self.userId)
        self.businessId = self.response_bs['business']['id']

        # add review by this user and for this business
        self.response = self.review.add_review(
            4, "Nice place for holidays", self.userId, self.businessId)

        # check whether this review exists in the data structure
        self.assertIn(self.response['review'], Review.reviews)

    def test_returns_all_reviews_for_business(self):
        # create a user
        self.response_user = self.user.add_user(
            'Test User', 'test@user.com', '1234pass')
        self.userId = self.response_user['user']['id']

        # create a business for this user
        self.response_bs = self.business.add_business(
            'Test Business1', 'Supermarket',
            'Behind Equity Bank', 'Githurai, Nairobi Area', self.userId)
        self.businessId = self.response_bs['business']['id']

        # add two reviews by this user and for this business
        self.review.add_review(
            4, "Nice place for holidays", self.userId, self.businessId)

        self.review.add_review(
            1, "Chefs are rude", self.userId, self.businessId)

        # check whether there are two reviews for this business
        # in the data structure
        self.reviews_for_bs = self.review.view_reviews_for(self.businessId)
        self.assertTrue(len(self.reviews_for_bs) == 2)
