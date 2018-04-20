import re


class Validator:
    def __init__(self):
        self.user_props = ['email', 'username', 'name', 'password']
        self.review_props = ['rating', 'body']
        self.business_props = ['name', 'description', 'location', 'category']
        self.has_numbers = re.compile('[0-9]')
        self.has_special = re.compile('[^\w\s]')
        self.categs = ['shop', 'supermarket', 'mall', 'school', 'church']

    def validate(self, obj, con):
        if con == 'user_reg':
            for prop in self.user_props:
                if prop not in obj:
                    return {"msg": "Missing details or invalid format"}
            for prop in self.user_props:
                if obj[prop].strip() == "":
                    return {'msg': 'Empty details not allowed'}
                if len(str(obj['name'])) < 4:
                    return {'msg': 'Name must be more than 4 characters'}
                if len(str(obj['name'])) > 255:
                    return {'msg': 'Name cannot be more than 255 characters'}
                if '@' not in str(obj['email']):
                    return {'msg': 'Email is invalid'}
                if len(str(obj['email'])) < 4:
                    return {'msg': 'Email cannot be less than 4 characters'}
                if len(str(obj['password'])) < 6:
                    return {'msg': 'Password cannot be less than 6 characters'}
                if len(str(obj['password'])) > 255:
                    return {'msg': 'Password cannot be more than 255 characters'}
                if len(str(obj['email'])) > 255:
                    return {'msg': 'Email cannot be more than 255 characters'}
                if len(str(obj['username'])) > 10:
                    return {'msg': 'Username cannot be more than 10 characters'}
                if self.has_numbers.search(obj['name']):
                    return {'msg': 'Name cannot contain numbers'}
                if self.has_special.search(obj['name']):
                    return {'msg': 'Name cannot contain special chars'}

        if con == 'business_reg':
            for prop in self.business_props:
                if prop not in obj:
                    return {"msg": "Missing details"}
            for prop in self.business_props:
                if obj[prop].strip() == "":
                    return {'msg': 'Empty details not allowed'}
                if len(str(obj['name'])) < 6:
                    return {'msg': 'Name must be more than 6 characters'}
                if len(str(obj['name'])) > 255:
                    return {'msg': 'Name must be less than 255 characters'}
                if len(str(obj['description'])) < 8:
                    return {'msg': 'Description must be more than 8 characters'}
                if len(str(obj['description'])) > 255:
                    return {'msg': 'Description must be less than 255 characters'}
                if self.has_numbers.search(obj['name']):
                    return {'msg': 'Name should not contain numbers or special chars'}
                if self.has_special.search(obj['description']):
                    return {'msg': 'Description should not contain special chars'}
                if self.has_special.search(obj['name']):
                    return {'msg': 'Name should not contain special chars'}
                if len(str(obj['location'])) > 255:
                    return {'msg': 'Location string must be less than 255 characters'}
                if obj['category'] not in self.categs:
                    return {'msg': 'Only businesses in {} are allowed'.format(str(self.categs))}

        if con == 'review_reg':
            for prop in self.review_props:
                if prop not in obj:
                    return {"msg": "Missing details or incorrect format"}
            for prop in self.review_props:
                if obj['body'].strip() == "":
                    return {'msg': 'Empty review not allowed'}
                if not isinstance(obj['rating'], int):
                    return {'msg': 'Rating must be values'}
                if len(str(obj['body'])) < 5:
                    return {'msg': 'Review must be more than 5 characters'}
                if len(str(obj['body'])) > 255:
                    return {'msg': 'Review must be less than 255 characters'}
                if int(obj['rating']) > 5:
                    return {'msg': 'Rating must be less than 5'}
