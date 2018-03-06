from datetime import datetime


class User(object):
    users = []
    user_logged_in = {}

    # creates a new user
    def add_user(self, name, username, email, password):
        self.created_on = str(datetime.now())
        self.user_dict = {
            'username': username,
            'name': name,
            'email': email,
            'password': password,
            'created on': self.created_on
            }
        self.users.append(self.user_dict)
        return {
            'user': self.user_dict,
            'msg': 'User created ok',
        }

    def view_user(self, username):
        for user in self.users:
            if user['username'] == username:
                return user
        return {
            'id': username,
            'msg': f'User with {username} not found'
        }
