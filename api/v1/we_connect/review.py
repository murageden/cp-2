from datetime import datetime
from we_connect.user import User


class Review(object):
    reviews = []

    def __init__(self):
        pass

    # adds a review
    def add_review(self, rating, body, username, businessId):
        self.id = 1

        self.created_on = str(datetime.now())

        if not len(Review.reviews) == 0:
            self.id = Review.reviews[-1]['id'] + 1

        self.review_dict = {
            'id': self.id,
            'rating': rating,
            'body': body,
            'review by': User.view_user(username),
            'businessId': businessId,
            'created on': self.created_on
        }

        self.reviews.append(self.review_dict)

        return self.review_dict

    # view a business' review
    def view_reviews_for(self, businessId):
        reviews_for = []

        for review in Review.reviews:
            if review['businessId'] == businessId:
                reviews_for.append(review)

        if reviews_for:
            return reviews_for
