from flask_login import UserMixin
from datetime import datetime, timedelta
import jwt

from app import db, app


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Plant %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, nullable=False, unique=True)
    email = db.Column(db.String(40), index=True, nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    plants = db.relationship('Plant', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_reset_password_token(self):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.utcnow() + timedelta(minutes=45)},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                         algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
