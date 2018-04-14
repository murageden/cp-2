"""we_connect/routes.py."""
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timedelta
from functools import wraps
import jwt

# local imports
from we_connect.models import User
from we_connect.models import Business
from we_connect.models import Review
from we_connect.validator import Validator
from run import app, db

validator = Validator()


def token_required(f):
    """Decorate a function to use a jwt token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'msg': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET'])
            current_user = User.get_user(data['username'])
            if current_user.logged_in == False:
                token = None
        except:
            return jsonify({'msg': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# creates a user account
@app.route('/weconnect/api/v2/auth/register', methods=['POST'])
def create_user():
    """Register a user into the API."""
    content = request.get_json(force=True)
    err_msg = validator.validate(content, 'user_reg')
    if err_msg:
        return jsonify(err_msg), 400
    if User.get_user(content['email'].strip()):
        return jsonify({'msg': 'Email already registered!'}), 400
    if User.get_user(content['username'].strip()):
        return jsonify({'msg': 'Username not available!'}), 400
    new_user = User(name=content['name'].strip(),
                    username=content['username'].strip(),
                    email=content['email'].strip(),
                    password=generate_password_hash(
                    content['password'].strip()))
    db.session.add(new_user)
    db.session.commit()
    created_user = User.get_user(content['email'].strip())
    message = {
        'details': {
            'name': created_user.name,
            'username': created_user.username,
            'email': created_user.email
        },
        'msg': "User {} created successfully on {}".format(
            created_user.username,
            created_user.date_created)
    }
    return jsonify(message), 201


@app.route('/weconnect/api/v2/auth/login', methods=['POST'])
def login_user():
    """Log in a user."""
    content = request.get_json(force=True)
    if 'username' in content:
        user = User.get_user(content['username'].strip())
    if 'email' in content:
        user = User.get_user(content['email'].strip())
    if not user:
        return jsonify({
            'msg': 'Email or username is incorrect'}), 400
    if check_password_hash(user.password, content['password']):
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.now() + timedelta(minutes=4)},
            app.config['SECRET'])
        return jsonify({
            'token': token.decode('UTF-8'),
            'msg': 'Log in successful'}), 200
    return jsonify({
        'msg': 'Wrong email or username/password combination'}), 400


@app.route('/weconnect/api/v1/auth/logout', methods=['POST'])
def logout():
    """Log out a user."""
    return jsonify({'msg': 'User log out successfull'}), 200


# password reset
@app.route('/weconnect/api/v2/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    """Change a password for a user."""
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    to_reset = current_user
    if 'old password' not in content:
        return jsonify({'msg': 'Missing old password'}), 400
    if 'new password' not in content:
        return jsonify({'msg': 'Missing new password'}), 400
    if not check_password_hash(to_reset.password,
                               content['old password'].strip()):
        return jsonify({
            'msg': 'Wrong password'}), 400
    User.query.filter_by(username=current_user.username).update(
        {'password': generate_password_hash(content['new password'].strip())})
    message = {
        'msg': 'Password for {} changed successfully'.format(to_reset.username)
    }
    return jsonify(message), 200


@app.route('/weconnect/api/v2/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    """Register a business for a user."""
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'business_reg')
    if message:
        return jsonify(message), 400
    new_business = Business(name=content['name'].strip(),
                            category=content['category'].strip(),
                            description=content['description'].strip(),
                            location=content['location'].strip(),
                            owner=current_user
                            )
    db.session.add(new_business)
    db.session.commit()
    message = {'msg': "Business id {} created for owner {}".format(
        new_business.id, new_business.business_owner),
        'details': {'name': new_business.name,
                    'category': new_business.category,
                    'description': new_business.description,
                    'location': new_business.location,
                    'owner': new_business.business_owner
                    }}
    return jsonify(message), 201


@app.route('/weconnect/api/v2/businesses/<business_id>', methods=['PUT'])
@token_required
def update_business(current_user, business_id):
    """Update an existing business."""
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'business_reg')
    if message:
        return jsonify(message), 400
    to_update = Business.query.filter_by(id=business_id).first()
    if not to_update:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    if not to_update.business_owner == current_user.username:
        return jsonify(
            {'msg': 'You are not allowed to edit this business'}), 403
    Business.query.filter_by(id=business_id).update(
        {
            'name': content['name'].strip(),
            'category': content['category'].strip(),
            'description': content['description'].strip(),
            'location': content['location'].strip(),
        })
    db.session.commit()
    updated_bs = Business.query.filter_by(id=business_id).first()
    message = {'msg': "Business id {} modified for owner {}".format(
        updated_bs.id, updated_bs.business_owner),
        'details': {'name': updated_bs.name,
                    'category': updated_bs.category,
                    'description': updated_bs.description,
                    'location': updated_bs.location,
                    'owner': updated_bs.business_owner
                    }}
    return jsonify(message), 201


@app.route('/weconnect/api/v2/businesses/<business_id>', methods=['DELETE'])
@token_required
def delete_business(current_user, business_id):
    """Remove an existing business."""
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    to_delete = Business.query.filter_by(id=business_id).first()
    if not to_delete:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    if not to_delete.business_owner == current_user.username:
        return jsonify(
            {'msg': 'You are not allowed to delete this business'}), 403
    db.session.delete(to_delete)
    db.session.commit()
    message = {'msg': 'Business id {} for owner {} deleted successfully'.
               format(to_delete.id, to_delete.business_owner),
               'details': {'name': to_delete.name,
                           'category': to_delete.category,
                           'description': to_delete.description,
                           'location': to_delete.location,
                           'owner': to_delete.business_owner
                           }}
    return jsonify(message), 200


@app.route('/weconnect/api/v2/businesses', methods=['GET'])
def get_all_businesses():
    """Retrieve the list of all businesses."""
    businesses = Business.query.all()
    if not businesses:
        return jsonify({'msg': 'No businesses yet'}), 200
    message = {'businesses': [{'name': business.name,
                               'category': business.category,
                               'description': business.description,
                               'location': business.location,
                               'owner': business.business_owner}
                              for business in businesses]}
    return jsonify(message), 200


@app.route('/weconnect/api/v2/businesses/<business_id>', methods=['GET'])
def get_business(business_id):
    """Retrieve a single business."""
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    message = {'msg': 'Business id {} owned by {} retrieved successfully'.
               format(business.id, business.business_owner),
               'details': {'name': business.name,
                           'category': business.category,
                           'description': business.description,
                           'location': business.location,
                           'owner': business.business_owner
                           }}
    return jsonify(message), 200


@app.route('/weconnect/api/v2/businesses/<business_id>/reviews',
           methods=['POST'])
@token_required
def add_review_for(current_user, business_id):
    """Add a review for a business."""
    if not current_user:
        return jsonify({'msg': 'Token is malformed'}), 400
    content = request.get_json(force=True)
    message = validator.validate(content, 'review_reg')
    if message:
        return jsonify(message), 400
    to_review = Business.query.filter_by(id=business_id).first()
    if not to_review:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    if to_review.business_owner == current_user.username:
        return jsonify({'msg': 'Review own business not allowed'}), 400
    review = Review(rating=content['rating'],
                    body=content['body'].strip(),
                    owner=current_user,
                    review_for=to_review)
    db.session.add(review)
    db.session.commit()
    message = {'msg': 'Review for business id {} by user {} created'.format(
        review.business_id, review.review_owner),
        'details': {'rating': review.rating,
                    'body': review.body}}
    return jsonify(message), 201


@app.route('/weconnect/api/v2/businesses/<business_id>/reviews',
           methods=['GET'])
def get_reviews_for(business_id):
    """Retrieve all reviews for a single business."""
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'msg': 'Business id is incorrect'}), 400
    reviews = Review.query.filter_by(business_id=business_id)
    if not reviews:
        return jsonify({'msg': 'No reviews for this business'}), 200
    message = {'reviews': [{'rating': review.rating,
                            'body': review.business_id,
                            'review by': review.review_owner}
                           for review in reviews],
               'business id': business.id,
               'business owner': business.business_owner}
    return jsonify(message)
