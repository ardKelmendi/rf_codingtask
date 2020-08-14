import flask_restless
from flask import  make_response
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from models import Category, Product, Sales

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# https://flask-restless.readthedocs.io/en/latest/quickstart.html

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)

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


if __name__ == "__main__":
    app.run()
