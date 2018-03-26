from datetime import datetime
from we_connect.user import User


class Review:
    """ a variable to hold all the reviews"""
    reviews = []

    def add_review(self, rating, body, username, businessId):
        """
            creates a review for a business and adds it to the list of review
            returns the added review
        """
        self.id = 1
        self.created_on = str(datetime.now())
        self.user = User.view_user(username)
        self.user_info = {
            'name': self.user['name'],
            'username': self.user['username'],
            'since': self.user['created on']
        }
        if not len(Review.reviews) == 0:
            self.id = Review.reviews[-1]['id'] + 1
        self.review_dict = {
            'id': self.id,
            'rating': rating,
            'body': body,
            'review by': self.user_info,
            'businessId': businessId,
            'created on': self.created_on}
        self.reviews.append(self.review_dict)
        return self.review_dict

    def view_reviews_for(self, businessId):
        """ reads a single review from teh reviews"""
        reviews_for = []
        for review in Review.reviews:
            if review['businessId'] == businessId:
                reviews_for.append(review)
        if reviews_for:
            return reviews_for
