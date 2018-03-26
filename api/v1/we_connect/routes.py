from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timedelta
from functools import wraps
import jwt

# local imports
from we_connect.user import User
from we_connect.business import Business
from we_connect.review import Review
from we_connect.validator import Validator

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'

business = Business()
user = User()
review = Review()
validator = Validator()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'msg': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.view_user(data['username'])
        except:
            return jsonify({'msg': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# creates a user account
@app.route('/weconnect/api/v1/auth/register', methods=['POST'])
def create_user():
    """
        registers a user into the API
    """
    content = request.get_json(force=True)
    message = validator.validate(content, 'user_reg')
    if message:
        return jsonify(message), 400
    if User.view_user(content['email']):
        return jsonify({'msg': 'Email already registered'}), 400
    if User.view_user(content['username']):
        return jsonify({'msg': 'Username not available'}), 400
    new_user = user.add_user(content['name'], content['username'],
    content['email'], generate_password_hash(content['password']))
    message = {
        'user': {
                    'name': new_user['name'],
                    'username': new_user['username'],
                    'email': new_user['email']
        },
        'msg': f"User created successfully on {new_user['created on']}"
    }
    return jsonify(message), 201


# logs in a user
@app.route('/weconnect/api/v1/auth/login', methods=['POST'])
def login_user():
    """
        logs in a user
    """
    content = request.get_json(force=True)
    if 'username' in content:
        user = User.view_user(content['username'])
    if 'email' in content:
        user = User.view_user(content['email'])
    if not user:
        return jsonify({
            'msg': 'Wrong email or username/password combination'}), 400
    if check_password_hash(user['password'], content['password']):
        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.now() + timedelta(minutes=4)},
            app.config['SECRET_KEY'])
        return jsonify({
            'token': token.decode('UTF-8'),
            'msg': 'Log in successful'}), 200
    return jsonify({
            'msg': 'Wrong email or username/password combination'}), 400


@app.route('/weconnect/api/v1/auth/logout', methods=['POST'])
def logout():
    return jsonify({'msg': 'User log out successfull'}), 200


# password reset
@app.route('/weconnect/api/v1/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    """
        changes a password for a user
    """
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    to_reset = User.view_user(current_user['username'])
    if not 'old password' in content:
        return jsonify({'msg': 'Missing old password'}), 400
    if not 'new password' in content:
        return jsonify({'msg': 'Missing new password'}), 400
    if not check_password_hash(to_reset['password'], content['old password']):
        return jsonify({
            'msg': 'Wrong old password'}), 400
    to_reset['password'] = generate_password_hash(content['new password'])
    reseted_user = User.view_user(current_user['username'])
    message = {
        'name': reseted_user['name'],
        'username': reseted_user['username'],
        'msg': 'Password changed successfully'
    }
    return jsonify(message)


@app.route('/weconnect/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    """
        registers a business for a user
    """
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'business_reg')
    if message:
        return jsonify(message), 400
    message = business.add_business(content['name'],
    content['category'], content['description'],
    content['location'], current_user['username'])
    return jsonify(message), 201


@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['PUT'])
@token_required
def update_business(current_user, businessId):
    """
        updates an existing business
    """
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'business_reg')
    if message:
        return jsonify(message), 400
    to_update = business.view_business(businessId)
    if to_update:
        if not to_update['owner']['username'] == current_user['username']:
            return jsonify(
                {'msg': 'You are not allowed to edit this business'}), 403
    message = business.update_business(
        businessId, content['name'], content['category'],
        content['description'], content['location'])
    if not message:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    return jsonify(message), 201


@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['DELETE'])
@token_required
def delete_business(current_user, businessId):
    """
        removes an existing business
        from the list of all businesses
    """
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    to_delete = business.view_business(businessId)
    if to_delete:
        if not to_delete['owner']['username'] == current_user['username']:
            return jsonify(
                {'msg': 'You are not allowed to delete this business'}), 403
    message = business.delete_business(businessId)
    if not message:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    return jsonify(message), 200


@app.route('/weconnect/api/v1/businesses', methods=['GET'])
def get_all_businesses():
    """
        retrieves the list of all businesses
    """
    businesses = Business.businesses
    if not len(businesses):
        return jsonify({'msg': 'No businesses yet'}), 200
    return jsonify(businesses), 200


@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['GET'])
def get_business(businessId):
    """
        retrieves a single business
        from the list of all businesses
    """
    message = business.view_business(businessId)
    if not message:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    return jsonify(message), 200


@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['POST'])
@token_required
def add_review_for(current_user, businessId):
    """
        adds a review to a business
    """
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'review_reg')
    if message:
        return jsonify(message), 400
    to_review = business.view_business(businessId)
    if not to_review:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    message = review.add_review(content['rating'],
    content['body'], current_user['username'], businessId)
    return jsonify(message), 201


@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['GET'])
def get_reviews_for(businessId):
    """
        retrieves all reviews for a single business
    """
    get_bs = business.view_business(businessId)
    if not get_bs:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    reviews = review.view_reviews_for(businessId)
    if not reviews:
        return jsonify({'msg': 'No reviews for this business'}), 200
    return jsonify(reviews), 200
