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
        return {
            'business': self.business_dict,
            'msg': 'Business created ok'
        }

    # reads a business
    def view_business(self, id):
        for business in Business.businesses:
            if str(business['id']) == str(id):
                return business

    # updates a business
    def update_business(self, id, name, category,
    description, location, owner):
        self.to_update = self.view_business(id)
        if self.to_update:
            self.to_update['name'] = name
            self.to_update['category'] = category
            self.to_update['description'] = description
            self.to_update['location'] = location

    # deletes a business
    def delete_business(self, id):
        self.to_remove = self.view_business(id)

        if self.to_remove:
            Business.businesses.remove(self.to_remove)

    # return businesses by loaction
    def search_business_by_location(self, location):
        pass

    # return businesses by category
    def search_business_by_location(self, location):
        pass

    # return all businesses
    def view_all_businesses(self):
        return Business.businesses
