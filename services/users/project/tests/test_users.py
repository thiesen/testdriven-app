import json
import unittest

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)

    db.session.add(user)
    db.session.commit()

    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual('pong!', data['message'])
        self.assertEqual('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'thiesen',
                    'email': 'thiesen@example.org'
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            print(data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual('thiesen@example.org was added!', data['message'])
            self.assertEqual('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertEqual('Invalid payload.', data['message'])
            self.assertEqual('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if username is not given."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'thiesen@example.org'}),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertEqual('Invalid payload.', data['message'])
            self.assertEqual('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if username is not given."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'thiesen',
                    'email': 'thiesen@example.org'
                }),
                content_type='application/json',
            )

            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'xunda',
                    'email': 'thiesen@example.org'
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                'Sorry. That email already exists.', data['message'])
            self.assertEqual('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('thiesen', 'thiesen@example.org')
        with self.client:
            response = self.client.get(f'/users/{user.id}')

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual('thiesen', data['data']['username'])
            self.assertEqual('thiesen@example.org', data['data']['email'])
            self.assertEqual('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if no id is given."""
        with self.client:
            response = self.client.get(f'/users/blah')

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertEqual('User does not exist.', data['message'])
            self.assertEqual('fail', data['status'])

    def test_single_user_invalid_id(self):
        """Ensure error is thrown if id does not exist"""
        with self.client:
            response = self.client.get(f'/users/9912319231')

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertEqual('User does not exist.', data['message'])
            self.assertEqual('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('xunda', 'xunda@example.org')
        add_user('dunha', 'dunha@example.org')

        with self.client:
            response = self.client.get('/users')

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertEqual('xunda', data['data']['users'][0]['username'])
            self.assertEqual(
                'xunda@example.org',
                data['data']['users'][0]['email']
            )
            self.assertEqual('dunha', data['data']['users'][1]['username'])
            self.assertEqual(
                'dunha@example.org',
                data['data']['users'][1]['email']
            )
            self.assertEqual('success', data['status'])


if __name__ == '__main__':
    unittest.main()
