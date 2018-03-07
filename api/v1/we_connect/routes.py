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
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.view_user(data['username'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# creates a user account
@app.route('/weconnect/api/v1/auth/register', methods=['POST'])
def create_user():
    content = request.get_json(force=True)

    if User.view_user(content['email']):
        return jsonify({'msg': 'Email already registered'}), 400

    if User.view_user(content['username']):
        return jsonify({'msg': 'Username not available'}), 400

    user = User()

    message = user.add_user(content['name'], content['username'],
    content['email'], generate_password_hash(content['password']))

    return jsonify(message), 201


# logs in a user
@app.route('/weconnect/api/v1/auth/login', methods=['POST'])
def login_user():
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
            'msg': 'Log in successful'}), 201


# logs out a user
@app.route('/weconnect/api/v1/auth/logout', methods=['POST'])
def logout():
    return jsonify({'msg': 'User log out successfull'}), 200


# password reset
@app.route('/weconnect/api/v1/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400

    content = request.get_json(force=True)

    user_to_reset = User.view_user(current_user['username'])

    user_to_reset['password'] = content['password']

    return jsonify(User.view_user(current_user['username']))


# register a business
@app.route('/weconnect/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400

    content = request.get_json(force=True)

    business = Business()

    message = business.add_business(content['name'],
    content['category'], content['description'],
    content['location'], current_user['username'])

    return jsonify(message), 201


# updates a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['PUT'])
@token_required
def update_business(current_user, businessId):
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400

    content = request.get_json(force=True)

    business = Business()

    to_update = business.view_business(businessId)

    if to_update:
        if not to_update['owner'] == current_user:
            return jsonify(
                {'msg': 'You are not allowed to edit this business'}), 403

    message = business.update_business(
        businessId, content['name'], content['category'],
        content['description'], content['location'])

    if not message:
        return jsonify({'msg': 'Business id is incorrect'}), 400

    return jsonify(message), 201


# removes a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['DELETE'])
@token_required
def delete_business(current_user, businessId):
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400

    content = request.get_json(force=True)

    business = Business()

    to_delete = business.view_business(businessId)

    if to_delete:
        if not to_delete['owner'] == current_user:
            return jsonify(
                {'msg': 'You are not allowed to delete this business'}), 403

    message = business.delete_business(businessId)

    if not message:
        return jsonify({'msg': 'Business id is incorrect'}), 400

    return jsonify(message), 201


# retrieves all businesses
@app.route('/weconnect/api/v1/businesses', methods=['GET'])
def get_all_businesses():
    businesses = Business.businesses

    if not len(businesses):
        return jsonify({'msg': 'No businesses yet'}), 200

    return jsonify(businesses), 200


# retrieves a single business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['GET'])
def get_business(businessId):
    business = Business()

    message = business.view_business(businessId)

    if not message:
        return jsonify({'msg': 'Business id is incorrect'}), 400

    return jsonify(message), 200


# adds a review to a business
@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['POST'])
@token_required
def add_review_for(current_user, businessId):
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400

    content = request.get_json(force=True)

    business = Business()

    business = business.view_business(businessId)

    if not business:
        return jsonify({'msg': 'Business id is incorrect'}), 400

    review = Review()

    message = review.add_review(content['rating'],
    content['body'], current_user['username'], businessId)

    return jsonify(message), 201


# retrieves all reviews for a single business
@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['GET'])
def get_reviews_for(businessId):
    business = Business()

    business = business.view_business(businessId)

    if not business:
        return jsonify({'msg': 'Business id is incorrect'}), 400

    review = Review()

    reviews = review.view_reviews_for(businessId)

    if not len(reviews):
        return jsonify({'msg': 'No reviews for this business'}), 200

    return jsonify(message), 200
