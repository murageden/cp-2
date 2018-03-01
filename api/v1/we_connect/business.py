class Business(object):
    businesses = []

    def __init__(self):
        pass

    # creates a business
    def create_business(self, name, category, description, location, ownerId):
        self.id = 1
        if not len(Business.businesses) == 0:
            self.id = Business.businesses[-1]['id'] + 1
        self.business_dict = {
            'id': self.id,
            'name': name,
            'category': category,
            'description': description,
            'location': location,
            'ownerId': ownerId,
            'msg': 'okay'
        }
        Business.businesses.append(self.business_dict)
        return {
            'id': self.id,
            'msg': 'Business id {} created successfully'.format(
                self.id)
        }

    # reads a business
    def view_business(self, id):
        for business in Business.businesses:
            if business['id'] == id:
                return business
        return {
            'id': id,
            'msg': 'Business id {} not found'.format(id)
        }

    # updates a business
    def update_business(
        self, id, name, category, description, location, ownerId):
        response = self.view_business(id)
        if not response['ownerId'] == ownerId:
            return {
                'status': 'error',
                'msg': 'You cannot update this business'
            }
        if response['msg'] == 'okay':
            response['name'] = name
            response['category'] = category
            response['description'] = description
            response['location'] = location
            return {
                'id': id,
                'msg': 'Business id {} modified successfully'.format(id)
            }
        return response
