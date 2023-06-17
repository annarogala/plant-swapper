from flask_login import UserMixin
from datetime import datetime, timedelta
import jwt

from app import db, app


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Plant %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, nullable=False, unique=True)
    email = db.Column(db.String(40), index=True, nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

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
