class Validator:
    def __init__(self):
        self.user_props = ['email', 'username', 'name', 'password']
        self.review_props = ['rating', 'body']
        self.business_props = ['name', 'description', 'location', 'category']

    def validate(self, obj, con):
        if con == 'user_reg':
            for prop in self.user_props:
               if prop not in obj:
                   return {"msg": "Missing details"}
            for prop in self.user_props:
                if obj[prop].strip() == "":
                    return {'msg': 'Empty details not allowed'}
        if con == 'business_reg':
            for prop in self.business_props:
               if prop not in obj:
                   return {"msg": "Missing details"}
            for prop in self.business_props:
                if obj[prop].strip() == "":
                    return {'msg': 'Empty details not allowed'}
        if con == 'review_reg':
            for prop in self.review_props:
               if prop not in obj:
                   return {"msg": "Missing details"}
            for prop in self.review_props:
                if obj['body'].strip() == "":
                    return {'msg': 'Empty values not allowed'}
                if obj['rating'] == None:
                    return {'msg': 'Empty values not allowed'}
                if not isinstance(obj['rating'], int):
                    return {'msg': 'Ratings must be values'}