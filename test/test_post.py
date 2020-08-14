# test_post.py
import pytest
from main import app
from flask import json, Flask
import unittest
from flask_testing import TestCase
from flask_testing import LiveServerTestCase


class MyTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

class MyTest(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


@pytest.fixture()
def test_add():        
    response = app.test_client().post(
        '/api/categories',
        data=json.dumps({'id': 1, 'name': 'ard'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['name'] == "ard"
