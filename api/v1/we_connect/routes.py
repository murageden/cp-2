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
        if not user.email == email:
            message = {
                'msg': 'Wrong email-password combination'
                }
            return jsonify(message)
        else:
            if user.password == password:
                message = {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'msg': 'Log in successfull'
                        }
                return jsonify(message)
