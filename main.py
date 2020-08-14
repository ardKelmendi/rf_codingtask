import flask_restless
from flask import Flask, make_response
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import Category, Product, Sales

from sqlalchemy import Column, Integer, Unicode
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm import scoped_session, sessionmaker

# https://flask-restless.readthedocs.io/en/latest/quickstart.html

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

engine = create_engine('sqlite:////tmp/testdb.sqlite', convert_unicode=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
mysession = scoped_session(Session)

Base = declarative_base()
Base.metadata.bind = engine


methods = ['GET', 'POST', 'PUT']

p = Product(1, 'ard')
p2 = Product(2, 'uran')

p_list = [p, p2]
s_list = [Sales(1, 10), Sales(1, 20)]
c_list = [Category(1, 100), Category(1, 200)]


@app.route('/')
@app.route('/api/<categories>/', methods=['GET'])
def handler(categories):
    if request.method == 'GET':
        return getCategory(categories)


@app.route('/')
@app.route('/api/<categories>/<int:request_id>', methods=['GET', 'PUT', 'POST'])
def productFunction(categories, request_id):
    if request.method == 'GET':
        return getCategory(categories)
    elif request.method == 'POST':
        req_data = request.get_json()
        id = req_data['id']
        title = req_data['name']
        # author = request.args.get('author', '')
        # genre = request.args.get('genre', '')
        found, target = requestInData(id)
        if found:
            return make_response(jsonify({"error": "Collection already exists"}), 400)
        return makeANewCategory(id, title)
    elif request.method == 'PUT':
        req_data = request.get_json()
        id = req_data['id']
        title = req_data['name']
        found, target = requestInData(request_id)
        if found:
            return update(target, title)
        else:
            return makeANewCategory(id, title)


def requestInData(id):
    for pl in p_list:
        if pl.id == id:
            return True, pl
    return False, None


def update(target, title):
    target.name = title
    return make_response(jsonify({"message": "Collection replaced"}), 200)
    # return jsonify(target.serialize)


def appendData(list):
    data =[]
    for pl in list:
        data.append(pl.serialize)
    return data


def getCategory(category):
    if category == "categories":
        data = appendData(c_list)
    elif category == "products":
        data = appendData(p_list)
    elif category == "sales":
        data = appendData(s_list)

    return jsonify(data)
    # category = session.query(Category).all()
    # return jsonify(category=[b.serialize for b in category])


def makeANewCategory(id, name):
    p = Product(id, name)
    p_list.append(p)
    return make_response(jsonify({"message": "Collection created"}), 201)
    # return jsonify(p.serialize)




# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.

if __name__ == "__main__":
    app.run()
