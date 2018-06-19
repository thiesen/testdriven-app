import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.utils import add_user
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('xunha', 'xunha@example.org')

        self.assertTrue(user.id)
        self.assertEqual(user.username, 'xunha')
        self.assertEqual(user.email, 'xunha@example.org')
        self.assertTrue(user.active)

    def test_add_user_dulicate_username(self):
        add_user('xunha', 'xunha@example.org')
        duplicate_user = User(
            username='xunha',
            email='xunda2@example.org'
        )

        db.session.add(duplicate_user)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_dulicate_email(self):
        add_user('xunha', 'xunha@example.org')
        duplicate_user = User(
            username='xunha2',
            email='xunha@example.org'
        )

        db.session.add(duplicate_user)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('xunha', 'xunha@example.org')

        self.assertTrue(isinstance(user.to_json(), dict))


if __name__ == '__main__':
    unittest.main()
