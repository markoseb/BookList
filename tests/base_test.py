"""
BaseTest

This class should be parent class to each non-unit test.
It allows for instantiation of the database dynamiclly
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from book_list import app
from book_list import db
import os



class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test_data.sqlite')
        with app.app_context():
            db.init_app(app)


    def setUp(self):
        # Make sure db exists

        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
