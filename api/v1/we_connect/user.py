class User(object):
    users = []

    def __init__(self):
        pass

    def create_user(self, name, email, password):
        self.id = 1
        if len(User.users):
            self.id = User.users[-1].id + 1
        self.user_dict = {
            'id': self.id,
            'name': name;
            'email': email,
            'password': password}
        self.users.append(self.user_dict)
        return {
            'id': self.id,
            'msg': 'User id {} created successfully'.format(self.id)
            }

    def get_all_users(self):
        return User.users
