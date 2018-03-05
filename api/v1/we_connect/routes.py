from flask import Flask, jsonify, request
# local imports
from we_connect.user import User
from we_connect.business import Business
from we_connect.review import Review

app = Flask(__name__)



# creates a user account
@app.route('/weconnect/api/v1/auth/register', methods=['POST'])
def create_user():
    content = request.get_json(force=True)
    user = User()
    message = user.create_user(content['name'],
    content['email'], content['password'])
    return jsonify(message)


# logs in a user
@app.route('/weconnect/api/v1/auth/login', methods=['POST'])
def login_user():
    content = request.get_json(force=True)
    user = User()
    all_users = user.get_all_users()
    message = {}
    for user in all_users:
        if user['email'] == content['email'] and user['password'] == content['password']:
            message = {
                        'id': user['id'],
                        'name': user['name'],
                        'email': user['email'],
                        'msg': 'Log in successfull'}
            User.user_logged_in = user
        if message:
            return jsonify(message)
    message = {
        'msg': 'Wrong email-password combination'}
    return jsonify(message)


# logs out a user
@app.route('/weconnect/api/v1/auth/logout', methods=['POST'])
def logout():
    if User.user_logged_in == {}:
        message = {
                'msg': 'No user is logged in currently'}
        return jsonify(message)
    else:
        message = {
                    'id': User.user_logged_in['id'],
                    'name': User.user_logged_in['name'],
                    'email': User.user_logged_in['email'],
                    'msg': 'Log out successfull'}
        User.user_logged_in = {}
        return jsonify(message)


# password reset
@app.route('/weconnect/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    userId = request.form.get('id')
    email = request.form.get('email')
    pass


# register a business
@app.route('/weconnect/api/v1/businesses', methods=['POST'])
def register_business():
    content = request.get_json(force=True)
    business = Business()
    message = business.create_business(content['name'], content['category'],
    content['description'], content['location'], content['ownerId'])
    return jsonify(message)


# updates a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['PUT'])
def update_business(businessId):
    content = request.get_json(force=True)
    business = Business()
    message = business.update_business(businessId, content['name'],
    content['category'], content['description'],
    content['location'], content['ownerId'])
    return jsonify(message)


# removes a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['DELETE'])
def remove_business(businessId):
    business = Business()
    message = business.delete_business(businessId)
    return jsonify(message)


# retrieves all businesses
@app.route('/weconnect/api/v1/businesses', methods=['GET'])
def retrieve_all_businesses():
    business = Business()
    message = business.view_all_businesses()
    return jsonify(message)


# retrieves a single business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['GET'])
def retrieve_business(businessId):
    response = Business().view_business(businessId)
    return jsonify(response)


# adds a review to a business
@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['POST'])
def add_review_for(businessId):
    content = request.get_json(force=True)
    review = Review()
    message = review.add_review(content['rating'],
    content['body'], content['userId'], content['businessId'])
    return jsonify(message)


# retrieves all reviews for a single business
@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['GET'])
def get_reviews_for(businessId):
    review = Review()
    message = review.view_reviews_for(businessId)
    return jsonify(message)


if(__name__) == '__main__':
    app.run(debug=True)
