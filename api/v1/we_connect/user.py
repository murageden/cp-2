from datetime import datetime


class User:
    """ class variable to hold all users """
    users = []

    def add_user(self, name, username, email, password):
        """
            creates a user and adds user into the users' list
            returns the added user
        """
        self.created_on = str(datetime.now())
        
        self.user_dict = {
            'username': username,
            'name': name,
            'email': email,
            'password': password,
            'created on': self.created_on
            }
        self.users.append(self.user_dict)
        
        return self.user_dict
    
    @staticmethod
    def view_user(username_or_email):
        """ reads a user by their username or email """
        for user in User.users:
            if user['username'] == username_or_email or user['email'] == username_or_email:
                return user
