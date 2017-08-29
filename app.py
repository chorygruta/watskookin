from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from flask_admin import Admin
import json
import sys


app = Flask(__name__)

app.config.from_pyfile('config.py')

heroku = Heroku(app)

db = SQLAlchemy(app)

ma = Marshmallow(app)

admin = Admin(app)

from views import *


if __name__ == '__main__':
    app.run(debug=True)

'''
Features

1. Log In
2. Search recipe by ingredients
3. Search recipe by keyword
4. recipe catalog (cuisine, dish type, diet)
'''
