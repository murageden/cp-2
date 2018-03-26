from datetime import datetime
from we_connect.user import User


class Business:
    """ class variable to hold all businesses """
    businesses = []

    def add_business(self, name, category, description, location, owner):
        """
            creates a business for a user, adds it to the list of businesses
            returns the added business
        """
        self.id = 1
        self.user = User.view_user(owner)
        self.user_info = {
            'name': self.user['name'],
            'username': self.user['username'],
            'since': self.user['created on']
        }
        self.created_on = str(datetime.now())
        if not len(self.businesses) == 0:
            self.id = self.businesses[-1]['id'] + 1
        self.business_dict = {
            'id': self.id,
            'name': name,
            'category': category,
            'description': description,
            'location': location,
            'owner': self.user_info,
            'created on': self.created_on}
        self.businesses.append(self.business_dict)
        return self.business_dict

    def view_business(self, id):
        """
            reads a single business from the list of businesses
            finds it by its id
        """
        for business in Business.businesses:
            if str(business['id']) == str(id):
                return business

    def update_business(self, id, name, category, description, location):
        """
            updates details of an existing business
            finds it by its id
        """
        self.to_update = self.view_business(id)
        if self.to_update:
            self.to_update['name'] = name
            self.to_update['category'] = category
            self.to_update['description'] = description
            self.to_update['location'] = location

            return self.view_business(id)

    def delete_business(self, id):
        """
            deletes a single business from the list of businesses
            finds it by its id
        """
        self.to_remove = self.view_business(id)
        if self.to_remove:
            Business.businesses.remove(self.to_remove)
            return self.to_remove

    def search_business_by_location(self, location):
        """
            searches for a single business from the list of businesses
            finds it by its loaction
        """
        self.in_this_location = []
        for business in Business.businesses:
            if business['location'] == location:
                self.in_this_location.append(business)
        return self.in_this_location

    def search_business_by_category(self, category):
        """
            searches for a single business from the list of businesses
            finds it by its category
        """
        self.in_this_categ = []
        for business in Business.businesses:
            if business['category'] == category:
                self.in_this_categ.append(business)
        return self.in_this_categ
