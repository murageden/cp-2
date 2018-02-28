from flask import Flask, jsonify, request

app = Flask(__name__)

# local imports
from we_connect.user import User

# creates a user account
@app.route('/weconnect/api/v1/auth/register', methods=['POST'])
def create_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User()
    message = user.create_user(name, email, password)
    return jsonify(message)
    