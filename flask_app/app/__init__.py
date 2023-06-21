from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os

from .config import Config


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config.from_object(Config)

mail = Mail(app)

from app import routes, models, login_form, config


if __name__ == "__main__":
    app.run(debug=True)
