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
s_list = [Sales(1, 10), Sales(2, 20)]
c_list = [Category(1, 100), Category(2, 200)]



@app.route('/')
@app.route('/api/<categories>/', methods=['GET'])
def handler(categories):
    if request.method == 'GET':
        query_params = normalize_query(request.args)
        if not query_params:
            return getRequest_all(categories)
        else:
            return return_queries(query_params)

def normalize_query_param(value):
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}


@app.route('/')
@app.route('/api/<categories>/<int:request_id>', methods=['GET', 'PUT', 'POST'])
def productFunction(categories, request_id):
    query_params = normalize_query(request.args)
    if request.method == 'GET':
        return getRequest_byId(categories, request_id)
    elif request.method == 'POST':
        req_data = request.get_json()
        id = req_data['id']
        title = req_data['name']
        found, target = requestInData(categories, id)
        if found:
            return make_response(jsonify({"error": "Collection already exists"}), 400)
        return makeANewCategory(id, title)
    elif request.method == 'PUT':
        req_data = request.get_json()
        id = req_data['id']
        title = req_data['name']
        found, target = requestInData(categories, request_id)
        if found:
            return update(target, title)
        else:
            return makeANewCategory(id, title)


# Implement an endpoint which can be used to select/filter the products by their quantity - using
# the greater_than and less_than query parameters.
def return_queries(args):
    assert len(['quantity_gt']) == 1
    assert len(['quantity_lt']) == 1
    left_bound = int(args['quantity_gt'])
    right_bound = int(args['quantity_lt'])
    data = []

    if "quantity_gt" in args and "quantity_lt" in args:
        for pl in s_list:
            if left_bound < pl.sales < right_bound:
                data.append(pl.serialize)
    elif "quantity_gt" in args:
        for pl in s_list:
            if left_bound < pl.sales:
                data.append(pl.serialize)
    elif "quantity_lt" in args:
        for pl in s_list:
            if pl.sales < right_bound:
                data.append(pl.serialize)
    else:
        return make_response(jsonify({"error": "query not supported"}), 404)

    if not data:
        return make_response(jsonify({"error": "no such product"}), 404)

    return jsonify(data)


def searchTarget(id, list):
    for pl in list:
        if pl.id == id:
            return True, pl
    return False, None


def requestInData(id, category):
    if category == "categories":
        return searchTarget(id, c_list)
    elif category == "products":
        return searchTarget(id, p_list)
    elif category == "sales":
        return searchTarget(id, s_list)


def update(target, title):
    target.name = title
    return make_response(jsonify({"message": "Collection replaced"}), 200)
    # return jsonify(target.serialize)


def appendData(list):
    data =[]
    for pl in list:
        data.append(pl.serialize)
    return data


def getRequest_byId(category, id):
    found, target = requestInData(id, category)
    if found:
        return jsonify(target.serialize)
    else:
        return make_response(jsonify({"error": "Id not found"}), 404)


def getRequest_all(category):
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
