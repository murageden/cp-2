import unittest
from we_connect.review import Review
from we_connect.user import User
from we_connect.business import Business


class reviewTestCase(unittest.TestCase):
    def setUp(self):
        self.review = Review()

    def test_create_review(self):
        self.response = self.review.add_review(
            4, "Nice place for holidays", 4, 1)

        self.assertIn(self.response, Review.reviews)

    def test_returns_all_reviews_for_business(self):
        self.review.add_review(
            4, "Nice place for holidays", 4, 1)

        self.review.add_review(
            1, "Chefs are rude", 4, 2)

        self.assertTrue(len(self.review.view_reviews_for(1)) == 2)
