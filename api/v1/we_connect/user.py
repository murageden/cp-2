from datetime import datetime


class User(object):
    users = []

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
    @staticmethod
    def view_user(username_or_email):
        for user in User.users:
            if user['username'] == username_or_email or user['email'] == username_or_email:
                return user