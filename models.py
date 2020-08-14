import flask_restless
from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json


app = Flask(__name__)

# https://flask-restless.readthedocs.io/en/latest/quickstart.html

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # to suppress a warning message
db = SQLAlchemy(app)


class Sales():
    def __init__(self, id, sales):
        self.id = id
        self.sales = sales

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.sales,
            # 'unit': self.unit,
            # 'quantity': self.quantity,
            # 'category': self.category,
            # 'measurement_unit': self.measurement_unit
        }

    # id = db.Column(db.Integer, primary_key=True)
    # product = db.Column(db.String(250))
    # sold_units = db.Column(db.Integer)
    # sold_date = db.Column(db.Date)


class Category():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name': self.name,
        }


class Product():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            # 'unit': self.unit,
            # 'quantity': self.quantity,
            # 'category': self.category,
            # 'measurement_unit': self.measurement_unit
        }


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class geeks:
    def __init__(self, id, name):
        self.id = id
        self.name = name


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


list_of = [geeks(1, 'Skr0'), geeks(2, 'Skr02')]
print('[')
for obj in list_of:
    print(obj.toJSON(), end='')
    print(',')
print(']')

# product = Object()
# product._isd = 2
# product._name = 'ASD'
# print(product.toJSON())

db.drop_all()
db.create_all()