class Review(object):
    reviews = []
    def __init__(self):
        pass

    # adds a review
    def add_review(self, rating, body, userId, businessId):
        self.id = 1
        if not len(reviews) == 0:
            self.id = Review.reviews[-1]['id'] + 1
        self.review_dict = {
            'id': self.id,
            'rating': rating,
            'body': body,
            'userId': userId,
            'businessId': businessId
        }
        Review.reviews.append(self.review_dict)
        return {
            'id': self.id,
            'msg': 'Review id {} created successfully'.format(self.id)
        }

    # view a business' review
    def view_reviews_for(self, businessId):
        for review in Review.reviews:
            if review['businessId'] == businessId:
                self.reviews_for = []
                self.reviews_for.append(review)
                return self.reviews_for
        return {
            'status': 'error',
            'msg': 'No reviews found for business id {}'.format(businessId)
        }