import datetime
from flask import  make_response
from flask import Flask, request, jsonify
from models import Category, Product, Sales


# https://flask-restless.readthedocs.io/en/latest/quickstart.html

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)

#simple `dataset`
p_list = [Product(1,'fish', '1234', '235', 'sea', 'kg'), Product(2,'chicken', '154', '25', 'meat', 'kg')]
s_list = [Sales(1, '512', 50, datetime.datetime(2020, 5, 17)), Sales(2, '512', 50, datetime.datetime(2019, 4, 17))]
c_list = [Category(1, 'import'), Category(2, 'export')]


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


def get_json_categories(req_data):
    id = req_data['id']
    name = req_data['name']
    return id,name


def get_json_products(req_data):
    id = req_data['id']
    name = req_data['name']
    unit = req_data['unit']
    quantity = req_data['quantity']
    category = req_data['category']
    measurement_unit = req_data['measurement_unit']
    return id, name, unit, quantity, category, measurement_unit


def get_json_sales(req_data):
    id = req_data['id']
    product = req_data['product']
    units_sold = req_data['units_sold']
    sold_date = req_data['sold_date']
    return id, product, units_sold, sold_date


def add_category(id, name):
    c_list.append(Category(id, name))
    return make_response(jsonify({"message": "Collection created"}), 201)
    # return jsonify(p.serialize)


def add_product(id, name, unit, quantity, category, measurement_unit):
    p_list.append(Product(id, name, quantity, category, measurement_unit))
    return make_response(jsonify({"message": "Collection created"}), 201)


def add_sale(id, product, units_sold, sold_date):
    s_list.append(Sales(id, product, units_sold, sold_date))
    return make_response(jsonify({"message": "Collection created"}), 201)



@app.route('/')
@app.route('/api/<categories>/<int:request_id>', methods=['GET', 'PUT', 'POST'])
def productFunction(categories, request_id):
    query_params = normalize_query(request.args)
    if request.method == 'GET':
        return getRequest_byId(categories, request_id)
    elif request.method == 'POST':
        req_data = request.get_json()
        if categories == "categories":
            c_id, c_name = get_json_categories(req_data)
            found, target = requestInData(c_id, categories)
            if found:
                return make_response(jsonify({"error": "Entity already exists"}), 400)
            add_category(c_id, c_name)

        elif categories == "products":
            p_id, p_name, p_unit, p_quantity, p_category, p_measurement_unit = get_json_products(req_data)
            found, target = requestInData(p_id, categories)
            if found:
                return make_response(jsonify({"error": "Entity already exists"}), 400)
            add_product(p_id, p_name, p_unit, p_quantity, p_category, p_measurement_unit)

        elif categories == "sales":
            s_id, s_product, s_units_sold, s_sold_date = get_json_sales(req_data)
            found, target = requestInData(s_id, categories)
            if found:
                return make_response(jsonify({"error": "Entity already exists"}), 400)
            add_sale(s_id, s_product, s_units_sold, s_sold_date)

    elif request.method == 'PUT':
        req_data = request.get_json()
        found, target = requestInData(request_id, categories)

        if categories == "categories":
            c_id, c_name = get_json_categories(req_data)
            if found:
                return update_category(target, c_id, c_name)
            else:
                return add_category(c_id, c_name)

        elif categories == "products":
            p_id, p_name, p_unit, p_quantity, p_category, p_measurement_unit = get_json_products(req_data)
            if found:
                return update_product(target, p_id, p_name, p_unit, p_quantity, p_category, p_measurement_unit)
            else:
                return add_product(p_id, p_name, p_unit, p_quantity, p_category, p_measurement_unit)

        elif categories == "sales":
            s_id, s_product, s_units_sold, s_sold_date = get_json_sales(req_data)
            if found:
                return update_sale(target, s_id, s_product, s_units_sold, s_sold_date)
            else:
                return add_sale(s_id, s_product, s_units_sold, s_sold_date)


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
            if left_bound < pl.units_sold < right_bound:
                data.append(pl.serialize)
    elif "quantity_gt" in args:
        for pl in s_list:
            if left_bound < pl.units_sold:
                data.append(pl.serialize)
    elif "quantity_lt" in args:
        for pl in s_list:
            if pl.units_sold < right_bound:
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
    else:
        return make_response(jsonify({"error": "Path not supported"}), 404)


def update_product(target, id, name, unit, quantity, category, measurement_unit):
    target.id = id
    target.name = name
    target.unit = unit
    target.quantity = quantity
    target.category = category
    target.measurement_unit = measurement_unit
    return make_response(jsonify({"message": "Collection replaced"}), 200)
    # return jsonify(target.serialize)


def update_category(target, id, name):
    target.id = id
    target.name = name
    return make_response(jsonify({"message": "Collection replaced"}), 200)


def update_sale(target, id, product, units_sold, sold_date):
    target.id = id
    target.product = product
    target.units_sold = units_sold
    return make_response(jsonify({"message": "Collection replaced"}), 200)



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




if __name__ == "__main__":
    app.run()
