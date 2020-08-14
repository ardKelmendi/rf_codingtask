# test_hello_add.py
from main import app
from flask import json


def test_add():        
    response = app.test_client().post(
        '/api/categories',
        data=json.dumps({'title': 1, 'title': 3}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['sum'] == 3


