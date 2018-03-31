"""we_connect/models.py."""
from run import db


class User(db.Model):
    """This class represents the user table."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    businesses = db.relationship('Business', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='owner', lazy=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              onupdate=db.func.current_timestamp())

    @staticmethod
    def get_user(username_or_email):
        """Retrieve a user."""
        query1 = User.query.filter_by(username=username_or_email).first()
        query2 = User.query.filter_by(email=username_or_email).first()
        return query1 or query2


class Business(db.Model):
    """This class represents the business table."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    business_owner = db.Column(db.String, db.ForeignKey('user.username'))
    reviews = db.relationship('Review', backref='review_for', lazy=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              onupdate=db.func.current_timestamp())


class Review(db.Model):
    """This class represents the review table."""

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    review_owner = db.Column(db.String, db.ForeignKey('user.username'))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              onupdate=db.func.current_timestamp())
