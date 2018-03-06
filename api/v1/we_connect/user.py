from datetime import datetime


class User(object):
    users = []
    user_logged_in = {}

    # creates a new user
    def add_user(self, name, email, password):
        self.id = 1
        self.created_on = str(datetime.now())
        if len(User.users):
            self.id = User.users[-1]['id'] + 1
        self.user_dict = {
            'id': self.id,
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

    def view_user(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        return {
            'id': id,
            'msg': f'User id {id} not found'
        }
