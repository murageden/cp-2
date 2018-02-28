class User(object):
    users = []
    def __init__(self):
        pass

    def create_user(self, name, email, password):
        self.id = 1
        if len(self.users):
            self.id = self.users[-1].id + 1
        self.name = name
        self.email = email
        self.password = password
        self.users.append(self)
        return {
            'id': self.id,
            'msg':'User id {} created successfully'.format(self.id)
            }