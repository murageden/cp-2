"""api/__init__.py."""
from flask import Flask, jsonify, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timedelta
from functools import wraps
import jwt

# local imports
from .users import User
from .businesses import Business
from .reviews import Review
from .validators import Validator

business = Business()
user = User()
review = Review()
validator = Validator()

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'


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
        except:
            return jsonify({'msg':
                            'Token is invalid, Please login to get a fresh token'}), 401
        current_user = User.view_user(data['username'])
        if not current_user:
            return jsonify({'msg':
                            'Token is invalid, Please login to get a fresh token'}), 401
        if not current_user['logged_in']:
            current_user = None
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/')
def home():
    return redirect("https://weconnnect.docs.apiary.io/", code=302)


@app.route('/api/v1/auth/register', methods=['POST'])
def create_user():
    """Registers a user into the API"""
    content = request.get_json(force=True)
    message = validator.validate(content, 'user_reg')
    if message:
        return jsonify(message), 400
    if User.view_user(content['email'].strip()):
        return jsonify({'msg': 'Email already registered'}), 400
    if User.view_user(content['username'].strip()):
        return jsonify({'msg': 'Username not available'}), 400
    new_user = user.add_user(content['name'].strip(), content['username'].strip(),
                             content['email'].strip().lower(), generate_password_hash(
        content['password'].strip()))
    message = {
        'user': {
            'name': new_user['name'],
            'username': new_user['username'],
            'email': new_user['email']
        },
        'msg': f"User created successfully on {new_user['created on']}"
    }
    return jsonify(message), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    """Logs in a user"""
    content = request.get_json(force=True)
    if 'username' in content:
        user = User.view_user(content['username'].strip())
    if 'email' in content:
        user = User.view_user(content['email'].strip().lower())
    if not user:
        return jsonify({
            'msg': 'Wrong email or username/password combination'}), 400
    if check_password_hash(user['password'], content['password'].strip()):
        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.now() + timedelta(minutes=300)},
            app.config['SECRET_KEY'])
        if user['logged_in'] == True:
            return jsonify({'token': token.decode('UTF-8'),
                            'msg': 'User already logged in'}), 400
        user['logged_in'] = True
        return jsonify({
            'token': token.decode('UTF-8'),
            'msg': 'Log in successful'}), 200
    return jsonify({
        'msg': 'Wrong email or username/password combination'}), 400


@app.route('/api/v1/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    if current_user == None:
        return jsonify({'msg': 'User already logged out'}), 200
    current_user['logged_in'] = False
    return jsonify({'msg': 'User log out successfull'}), 200


@app.route('/api/v1/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    """Changes a password for a user"""
    if current_user == None:
        return jsonify({'msg': 'Token is invalid, Please login to get a fresh token'}), 400
    content = request.get_json(force=True)
    to_reset = User.view_user(current_user['username'])
    if not 'old password' in content:
        return jsonify({'msg': 'Missing old password'}), 400
    if not 'new password' in content:
        return jsonify({'msg': 'Missing new password'}), 400
    if not check_password_hash(to_reset['password'], content['old password'].strip()):
        return jsonify({
            'msg': 'Wrong old password'}), 400
    to_reset['password'] = generate_password_hash(
        content['new password'].strip())
    reseted_user = User.view_user(current_user['username'])
    message = {
        'name': reseted_user['name'],
        'username': reseted_user['username'],
        'msg': 'Password changed successfully'
    }
    return jsonify(message)


@app.route('/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    """Registers a business for a user"""
    if current_user == None:
        return jsonify({'msg': 'Token is invalid, Please login to get a fresh token'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'business_reg')
    if message:
        return jsonify(message), 400
    new_bs = business.add_business(content['name'].strip(),
                                   content['category'].strip(
    ), content['description'].strip(),
        content['location'].strip(), current_user['username'])
    message = {
        'msg': f'Business id {new_bs["id"]} created successfully',
                'details': new_bs
    }
    return jsonify(message), 201


@app.route('/api/v1/businesses/<businessId>', methods=['PUT'])
@token_required
def update_business(current_user, businessId):
    """Updates an existing business"""
    if current_user == None:
        return jsonify({'msg': 'Token is invalid, Please login to get a fresh token'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'business_reg')
    if message:
        return jsonify(message), 400
    to_update = business.view_business(businessId)
    if to_update:
        if not to_update['owner']['username'] == current_user['username']:
            return jsonify(
                {'msg': 'You are not allowed to edit this business'}), 403
    updated_bs = business.update_business(
        businessId, content['name'].strip(), content['category'].strip(),
        content['description'].strip(), content['location'].strip())
    if not updated_bs:
        return jsonify({'msg': 'Business for id provided does not exist'}), 400
    message = {
        'msg': f'Business id {updated_bs["id"]} updated successfully',
                'details': updated_bs
    }
    return jsonify(message), 201


@app.route('/api/v1/businesses/<businessId>', methods=['DELETE'])
@token_required
def delete_business(current_user, businessId):
    """Removes an existing business from the list of all businesses"""
    if current_user == None:
        return jsonify({'msg': 'Token is invalid, Please login to get a fresh token'}), 400
    to_delete = business.view_business(businessId)
    if to_delete:
        if not to_delete['owner']['username'] == current_user['username']:
            return jsonify(
                {'msg': 'You are not allowed to delete this business'}), 403
    deleted_bs = business.delete_business(businessId)
    if not deleted_bs:
        return jsonify({'msg': 'Business for id provided does not exist'}), 400
    message = {
        'msg': f'Business id {deleted_bs["id"]} deleted successfully',
                'details': deleted_bs
    }
    return jsonify(message), 200


@app.route('/api/v1/businesses', methods=['GET'])
def get_all_businesses():
    """Retrieves the list of all businesses"""
    businesses = Business.businesses
    if not len(businesses):
        return jsonify({'msg': 'No businesses yet'}), 200
    return jsonify(businesses), 200


@app.route('/api/v1/businesses/<businessId>', methods=['GET'])
def get_business(businessId):
    """Retrieves a single business from the list of all businesses"""
    bs = business.view_business(businessId)
    if not bs:
        return jsonify({'msg': 'Business for id provided does not exist'}), 400
    message = {
        'msg': f'Business id {bs["id"]} retrieved successfully',
                'details': bs
    }
    return jsonify(message), 200


@app.route('/api/v1/businesses/<businessId>/reviews',
           methods=['POST'])
@token_required
def add_review_for(current_user, businessId):
    """Adds a review to a business"""
    if current_user == None:
        return jsonify({'msg': 'Token is invalid, Please login to get a fresh token'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'review_reg')
    if message:
        return jsonify(message), 400
    to_review = business.view_business(businessId)
    if not to_review:
        return jsonify({'msg': 'Business for id provided does not exist'}), 400
    if to_review['owner']['username'] == current_user['username']:
        return jsonify({'msg': 'Review own business not allowed'}), 400
    added_review = review.add_review(content['rating'],
                                     content['body'].strip(),
                                     current_user['username'], businessId)
    message = {
        'msg': f'Review added successfully',
                'details': added_review
    }
    return jsonify(message), 201


@app.route('/api/v1/businesses/<businessId>/reviews',
           methods=['GET'])
def get_reviews_for(businessId):
    """Retrieves all reviews for a single businesss"""
    get_bs = business.view_business(businessId)
    if not get_bs:
        return jsonify({'msg': 'Business for id provided does not exist'}), 400
    reviews = review.view_reviews_for(businessId)
    if not reviews:
        return jsonify({'msg': 'No reviews for this business'}), 200
    return jsonify(reviews), 200
