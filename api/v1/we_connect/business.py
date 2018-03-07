from datetime import datetime
from we_connect.user import User


class Business:
    # list variable to hold all businesses
    businesses = []

    # creates a business
    def add_business(self, name, category, description, location, owner):
        self.id = 1
        self.user = User()
        self.created_on = str(datetime.now())
        if not len(self.businesses) == 0:
            self.id = self.businesses[-1]['id'] + 1
        self.business_dict = {
            'id': self.id,
            'name': name,
            'category': category,
            'description': description,
            'location': location,
            'owner': User.view_user(owner),
            'created on': self.created_on}

        self.businesses.append(self.business_dict)
        
        return self.business_dict

    # reads a business
    def view_business(self, id):
        for business in Business.businesses:
            if str(business['id']) == str(id):
                return business

    # updates a business
    def update_business(self, id, name, category, description, location):
        self.to_update = self.view_business(id)
        if self.to_update:
            self.to_update['name'] = name
            self.to_update['category'] = category
            self.to_update['description'] = description
            self.to_update['location'] = location
            return {
                'business': self.view_business(id),
                'msg': 'Business updated ok'
            }

    # deletes a business
    def delete_business(self, id):
        self.to_remove = self.view_business(id)

        if self.to_remove:
            Business.businesses.remove(self.to_remove)
            return self.to_remove

    # return businesses by loaction
    def search_business_by_location(self, location):
        self.in_this_location = []

        for business in Business.businesses:
            if business['location'] == location:
                self.in_this_location.append(business)

        return self.in_this_location

    # return businesses by category
    def search_business_by_category(self, category):
        self.in_this_categ = []

        for business in Business.businesses:
            if business['category'] == category:
                self.in_this_categ.append(business)

        return self.in_this_categ
