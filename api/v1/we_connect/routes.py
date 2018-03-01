from flask import Flask, jsonify, request
# local imports
from we_connect.user import User

app = Flask(__name__)


# creates a user account
@app.route('/weconnect/api/v1/auth/register', methods=['POST'])
def create_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User()
    message = user.create_user(name, email, password)
    return jsonify(message)


# logs in a user
@app.route('/weconnect/api/v1/auth/login', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User()
    all_users = user.get_all_users()
    for user in all_users:
        if user['email'] == email and user['password'] == password:
            message = {
                        'id': user['id'],
                        'name': user['name'],
                        'email': user['email'],
                        'msg': 'Log in successfull'}
            return jsonify(message)
        else:
            message = {
                'msg': 'Wrong email-password combination'}
            return jsonify(message)


# logs out a user
@app.route('/weconnect/api/v1/auth/logout', methods=['POST'])
def logout():
    pass


# password reset
@app.route('/weconnect/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    pass


# register a business
@app.route('/weconnect/api/v1/businesses', methods=['POST'])
def register_business():
    pass


# updates a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['PUT'])
def update_business():
    pass


# removes a business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['DELETE'])
def remove_business():
    pass


# retrieves all businesses
@app.route('/weconnect/api/v1/businesses', methods=['GET'])
def retrieve_all_businesses():
    pass


# retrieves a single business
@app.route('/weconnect/api/v1/businesses/<businessId>', methods=['GET'])
def retrieve_business(businessId):
    business = Business().get_business(businessId)
    return jsonify({'business': business})


# adds a review to a business
@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['POST'])
def add_review_for(businessId):
    pass


# retrieves all reviews for a single business
@app.route('/weconnect/api/v1/businesses/<businessId>/reviews',
methods=['GET'])
def get_reviews_for(businessId):
    pass


if(__name__) == '__main__':
    app.run(debug=True)
