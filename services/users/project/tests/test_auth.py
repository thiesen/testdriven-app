import json

from flask import current_app

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'thiesen',
                    'email': 'thiesen@example.org',
                    'password': 'xunda',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        add_user('xunda', 'thiesen@example.org', 'xunda')

        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'thiesen',
                    'email': 'thiesen@example.org',
                    'password': 'xunda',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'],
                'Sorry. That user already exists.'
            )
            self.assertEqual(response.status_code, 400)

    def test_user_registration_duplicate_username(self):
        add_user('thiesen', 'thiesen@example.org', 'xunda')

        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'thiesen',
                    'email': 'xunda@example.org',
                    'password': 'xunda',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'],
                             'Sorry. That user already exists.')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_invalid_json_no_username(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'xunda@example.org',
                    'password': 'xunda',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_invalid_json_no_email(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'thiesen',
                    'password': 'xunda',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Invalid payload.')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_invalid_json_no_password(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'thiesen',
                    'email': 'thiesen@example.org',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            print(data['status'])
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'Invalid payload.')

    def test_registered_user_login(self):
        add_user('thiesen', 'thiesen@example.org', 'xunda')

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'thiesen@example.org',
                    'password': 'xunda',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'thiesen',
                    'password': 'xunda',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'User does not exist.')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.content_type, 'application/json')

    def test_valid_logout(self):
        add_user('test', 'test@test.com', 'test')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                }),
                content_type='application/json'
            )

            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

        def test_invalid_logout_expired_token(self):
            current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
            add_user('test', 'test@test.com', 'test')

            with self.client:
                resp_login = self.client.post(
                    '/auth/login',
                    data=json.dumps({
                        'email': 'test@test.com',
                        'password': 'test',
                    }),
                    content_type='application/json'
                )

                token = json.loads(resp_login.data.decode.get('auth_token'))

                response = self.client.get(
                    '/auth/logout',
                    headers={'Authorization': f'Bearer {token}'}
                )

                data = json.loads(response.data.decode())

                self.assertEqual(data['status'], 'fail')
                self.assertEqual(
                    data['message'], 'Signature expired. Please log in again.')
                self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer invalid'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'], 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        add_user('test', 'test@test.com', 'test')

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                }),
                content_type='application/json'
            )

            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data']['username'], 'test')
            self.assertEqual(data['data']['email'], 'test@test.com')
            self.assertTrue(data['data']['active'])
            self.assertEqual(response.status_code, 200)

    def test_user_status_invalid_token(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer invalid'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(
                data['message'], 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)
