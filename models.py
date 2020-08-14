#Class contains 3 classes that are used to store the data

class Product:
    def __init__(self, id, name, unit, quantity, category, measurement_unit):
        self.id = id
        self.name = name
        self.unit = unit
        self.quantity = quantity
        self.category = category
        self.measurement_unit = measurement_unit

    '''method to return a JSON format'''
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'quantity': self.quantity,
            'category': self.category,
            'measurement_unit': self.measurement_unit
        }


class Sales:
    def __init__(self, id, product, units_sold, sold_date):
        self.id = id
        self.product = product
        self.units_sold = units_sold
        self.sold_date = sold_date

    '''method to return a JSON format'''
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.product,
            'units sold': self.units_sold,
            'sold date': self.sold_date,
        }


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    '''method to return a JSON format'''
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name': self.name,
        }