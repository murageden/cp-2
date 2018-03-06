from datetime import datetime
from we_connect.user import User


class Business(object):
    businesses = []

    def __init__(self):
        pass

    # creates a business
    def add_business(self, name, category, description, location, ownerId):
        self.id = 1
        self.user = User()
        self.created_on = str(datetime.now())
        if not len(Business.businesses) == 0:
            self.id = Business.businesses[-1]['id'] + 1
        self.business_dict = {
            'id': self.id,
            'name': name,
            'category': category,
            'description': description,
            'location': location,
            'owner': self.user.view_user(ownerId),
            'msg': 'okay',
            'created on': self.created_on
        }
        self.businesses.append(self.business_dict)
        return {
            'business': self.business_dict,
            'msg': 'Business created ok'
        }

    # reads a business
    def view_business(self, id):
        for business in Business.businesses:
            if business['id'] == id:
                return business
        return {
            'id': id,
            'msg': f'Business id {id} not found'
        }

    # updates a business
    def update_business(self, id, name, category,
    description, location, ownerId):
        self.response = self.view_business(id)
        if self.response['msg'] == 'okay':
            if not self.response['ownerId'] == ownerId:
                return {
                    'status': 'error',
                    'msg': 'You cannot update this business'
                }
            self.response['name'] = name
            self.response['category'] = category
            self.response['description'] = description
            self.response['location'] = location
            return {
                'id': id,
                'msg': f'Business id {id} modified successfully'
            }
            return self.response

    # deletes a business
    def delete_business(self, id):
        self.response = self.view_business(id)
        if self.response['msg'] == 'okay':
            Business.businesses.remove(self.response)
            return {
                'id': self.response['id'],
                'msg': f'Business id {self.response["id"]} deleted successfully'
            }
        return self.response

    # return businesses by loaction
    def search_business_by_location(self, location):
        pass

    # return businesses by category
    def search_business_by_location(self, location):
        pass

    # return all businesses
    def view_all_businesses(self):
        return Business.businesses
