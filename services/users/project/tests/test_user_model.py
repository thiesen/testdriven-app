import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.utils import add_user
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('xunha', 'xunha@example.org', 'xunda')

        self.assertTrue(user.id)
        self.assertEqual(user.username, 'xunha')
        self.assertEqual(user.email, 'xunha@example.org')
        self.assertTrue(user.active)

    def test_add_user_dulicate_username(self):
        add_user('xunha', 'xunha@example.org', 'xunda')
        duplicate_user = User(
            username='xunha',
            email='xunda2@example.org',
            password='xunda',
        )

        db.session.add(duplicate_user)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_dulicate_email(self):
        add_user('xunha', 'xunha@example.org', 'xunda')
        duplicate_user = User(
            username='xunha2',
            email='xunha@example.org',
            password='xunda',
        )

        db.session.add(duplicate_user)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('xunha', 'xunha@example.org', 'xunda')

        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user = add_user('thiesen', 'thiesen@example.org', 'xunda')
        another_user = add_user('thiesen2', 'thiesen2@example.org', 'xunda')

        self.assertNotEqual(user.password, another_user.password)

    def test_encode_auth_token(self):
        user = add_user('thiesen', 'thiesen@example.org', 'xunda')

        auth_token = User.encode_auth_token(user.id)

        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('thiesen', 'thiesen@example.org', 'xunda')

        auth_token = User.encode_auth_token(user.id)

        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(user.id, User.decode_auth_token(auth_token))


if __name__ == '__main__':
    unittest.main()
