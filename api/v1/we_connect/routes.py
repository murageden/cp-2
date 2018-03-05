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
    message = user.add_user(content['name'],
    content['email'], content['password'])
    return jsonify(message), 201


# logs in a user
@app.route('/weconnect/api/v1/auth/login', methods=['POST'])
def login_user():
    if User.user_logged_in:
        return jsonify({
            'msg': 'A user is logged in already'
        }) 
    content = request.get_json(force=True)
    message = {}
    for user in User.users:
        if user['email'] == content['email'] and user['password'] == content['password']:
            message = {
                        'id': user['id'],
                        'name': user['name'],
                        'email': user['email'],
                        'msg': 'Log in successfull'}
            User.user_logged_in = user
        if message:
            return jsonify(message), 201
    message = {
        'msg': 'Wrong email-password combination'}
    return jsonify(message)


# logs out a user
@app.route('/weconnect/api/v1/auth/logout', methods=['POST'])
def logout():
    if User.user_logged_in == {}:
        return jsonify({
                'msg': 'No user is logged in currently'})
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
    if User.user_logged_in == {}:
        return jsonify({
                'msg': 'You have to be logged in'})
    content = request.get_json(force=True)
    for user in User.users:
        if user['email'] == content['email']:
            user['password'] = content['password']
            return jsonify({'msg': 'Password changed successfully'}), 201
    return jsonify({'msg': 'Email provided is incorrect'})
    

# register a business
@app.route('/weconnect/api/v1/businesses', methods=['POST'])
def register_business():
    if User.user_logged_in == {}:
        return jsonify({
                'msg': 'You must log in first'})
    content = request.get_json(force=True)
    business = Business()
    message = business.add_business(content['name'],
    content['category'], content['description'],
    content['location'], User.user_logged_in['id'])
    return jsonify(message), 201


# updates a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['PUT'])
def update_business(businessId):
    if User.user_logged_in == {}:
        return jsonify({
                'msg': 'You must log in first'})
    content = request.get_json(force=True)
    business = Business()
    message = business.update_business(
        businessId, content['name'], content['category'],
        content['description'], content['location'],
        User.user_logged_in['id'])
    return jsonify(message), 201


# removes a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['DELETE'])
def delete_business(businessId):
    if User.user_logged_in == {}:
        return jsonify({
                'msg': 'You must log in first'})
    content = request.get_json(force=True)
    business = Business()
    message = business.delete_business(businessId)
    return jsonify(message)

# retrieves all businesses
@app.route('/weconnect/api/v1/businesses', methods=['GET'])
def get_all_businesses():
    businesses = Business.businesses
    jsonify(businesses)


# retrieves a single business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['GET'])
def get_business(businessId):
    business = Business()
    message = business.view_business(businessId)
    return jsonify(message)

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
