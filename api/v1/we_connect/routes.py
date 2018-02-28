from flask import Flask, jsonify, request

app = Flask(__name__)

# local imports
from we_connect.business import Business
from we_connect.review import Review
from we_connect.user import User

# creates a user account
@app.route('/weconnect/api/v1/auth/register', methods=['POST'])
def create_user():
    pass
    