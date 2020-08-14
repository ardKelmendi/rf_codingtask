import json


class Sales:
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


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name': self.name,
        }


class Product:
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
