from datetime import datetime


class User:
    """ class variable to hold all users """
    users = []

    def add_user(self, name, username, email, password):
        """Creates a user and adds user into the users' list returns the added users"""
        self.created_on = str(datetime.now())
        
        self.user_dict = {
            'username': username,
            'name': name,
            'email': email,
            'password': password,
            'logged_in': False,
            'created on': self.created_on
            }
        self.users.append(self.user_dict)
        
        return self.user_dict
    
    @staticmethod
    def view_user(username_or_email):
        """Reads a user by their username or emails"""
        for user in User.users:
            if user['username'] == username_or_email or user['email'] == username_or_email:
                return user
