import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')

        return app

    def test_app_is_development(self):
        self.assertEqual(app.config['SECRET_KEY'], 'my_precious')
        self.assertFalse(current_app is None)
        self.assertFalse(app.config['TESTING'])
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'],
            os.environ.get('DATABASE_URL')
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')

        return app

    def test_app_is_testing(self):
        self.assertEqual(app.config['SECRET_KEY'], 'my_precious')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(current_app is None)
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'],
            os.environ.get('DATABASE_TEST_URL')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')

        return app

    def test_app_is_production0(self):
        self.assertEqual(app.config['SECRET_KEY'], 'my_precious')
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
