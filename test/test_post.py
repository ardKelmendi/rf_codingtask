# test_post.py
from main import app
from flask import json


def test_add():        
    response = app.test_client().post(
        '/api/categories',
        data=json.dumps({'id': 1, 'name': 'ard'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['name'] == "ard"

