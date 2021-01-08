from base64 import b64encode
from datetime import datetime, timedelta
import json
import re
import unittest
from app import create_app, db
from app.models import User, Post
from tests import TestConfig

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        ''' test 404 Error handle '''
        response = self.client.get('/api/wrong/url')
        self.assertEqual(404, response.status_code)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'Not Found')

    def get_basic_auth_headers(self, username, password):
        ''' Create headers for basic auth '''
        return {
            'Authorization': 'Basic' + b64encode(
                (username + ':' + password).encode('utf-8')
            ).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_token_auth_headers(self, username, password):
        ''' Create JSON web token headers '''
        headers = self.get_basic_auth_headers(username, password)
        response = self.client.post('/api/tokens', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']
        return {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_token(self):
        ''' Create a test user '''
        u = User(username='john', email='john@163.com')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()

        ''' Input wrong password '''
        headers = self.get_basic_auth_headers('john', '456')
        response = self.client.post('/api/tokens', headers=headers)
        self.assertEqual(response.status_code, 401)

        ''' Input correct password '''
        headers = self.get_basic_auth_headers('john', '123')
        response = self.client.post('/api/tokens', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        self.assertTrue(re.match(r'(.+)\.(.+)\.(.+)', json_response.get('token')))

    def test_not_attach_jwt(self):
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 401)

    def test_attach_jwt(self):
        u = User(username='john', email='john@163.com')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()
        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)

    def test_anonymous(self):
        response = self.client.get('/api/posts')
        self.assertEqual(response.status_code, 200)
