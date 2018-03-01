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
            'ownerId': ownerId
        }
        Business.businesses.append(self.business_dict)
        return {
            'id': self.id,
            'msg': 'Business id {} created successfully'.format(
                self.id)
        }