"""we_connect/validator.py."""
import re


class Validator:
    """Object to contain all the validation rules and methods."""

    def __init__(self):
        """Validation rules."""
        self.user_props = ['email', 'username', 'name', 'password']
        self.review_props = ['rating', 'body']
        self.business_props = ['name', 'description', 'location', 'category']
        self.has_numbers = re.compile('[0-9]')
        self.has_special = re.compile('[^\w\s]')
        self.categs = ['shop', 'supermarket', 'mall', 'school', 'church']

    def validate(self, obj, con):
        """Method that validates the rules."""
        if con == 'user_reg':
            for prop in self.user_props:
                if prop not in obj:
                    return {"msg": "Missing details"}
            for prop in self.user_props:
                if obj[prop].strip() == "":
                    return {'msg': 'Empty details not allowed'}
            if not 6 < len(str(obj['name'])):
                return {'msg': 'Name should be more than 6 characters'}
            if '@' not in str(obj['email']):
                return {'msg': 'Email is invalid'}
            if len(str(obj['email'])) < 4:
                return {'msg': 'Email is invalid'}
            if not 4 < len(str(obj['username'])) < 10:
                return {'msg': 'Username should be between\
                4 and 10 characters'}
            if self.has_numbers.search(obj['name']):
                return {'msg': 'Name should not contain numbers'}
            if self.has_special.search(obj['name']):
                return {'msg': 'Name should not contain special chars'}

        if con == 'business_reg':
            for prop in self.business_props:
                if prop not in obj:
                    return {"msg": "Missing details"}
            for prop in self.business_props:
                if obj[prop].strip() == "":
                    return {'msg': 'Empty details not allowed'}
            if not 6 < len(str(obj['name'])):
                return {'msg': 'Name should be more than 6 characters'}
            if not 8 < len(str(obj['description'])):
                return {'msg': 'Description should be more than 8 characters'}
            if self.has_numbers.search(obj['name']):
                return {'msg': 'Name should not contain\
                numbers or special characters'}
            if self.has_special.search(obj['description']):
                return {'msg': 'Description should not contain special chars'}
            if self.has_special.search(obj['name']):
                return {'msg': 'Name should not contain special chars'}
            if obj['category'] not in self.categs:
                return {'msg': 'Only businesses\
                in {} are allowed'}.format(str(self.categs))

        if con == 'review_reg':
            for prop in self.review_props:
                if prop not in obj:
                    return {"msg": "Missing details"}
            for prop in self.review_props:
                if obj['body'].strip() == "":
                    return {'msg': 'Empty values not allowed'}
                if not isinstance(obj['rating'], int):
                    return {'msg': 'Ratings must be values'}
                if not 6 < len(str(obj['body'])):
                    return {'msg': 'Body should be more than 6 characters'}
