import unittest
from flask import current_app
from app import create_app, db
from tests import TestConfig

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        ''' Execute before any tests '''
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        ''' Execute after any tests '''
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])