from pyramid.httpexceptions import HTTPBadRequest

from sec_1_api.lib.security import hash_password, check_password
from sec_1_api.tests import TestCase, UnitTestCase, FunctionalTestCase


class EncryptTest(TestCase):

    def setUp(self):
        self.test_password = 'test123'

    def test_hash_password(self):
        hashed_password, salt = hash_password(self.test_password)
        self.assertIsNotNone(hashed_password)
        self.assertIsNotNone(salt)

    def test_check_password(self):
        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        try:
            check_password('test123', hashed_password, salt)
        except HTTPBadRequest:
            self.fail("check_password raised HTTPBadRequest unexpectedly")

        with self.assertRaises(HTTPBadRequest):
            check_password('notrightpass', hashed_password, salt)


class TestAuthHandlers(UnitTestCase):

    def test_login_succesful(self):
        from sec_1_api.models.user import User
        from sec_1_api.handlers.auth import login
        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        user = User(username='test',
                    password_hash=hashed_password,
                    password_salt=salt)
        self.session.add(user)
        self.session.flush()

        request = self.get_post_request(post={
            'username': 'test',
            'password': 'test123'
        })

        login(request)
        self.assertEqual(request.response.status_code, 200)


class FunctionalTestAuthHandlers(FunctionalTestCase):

    def test_login_succesful(self):
        from sec_1_api.models.user import User
        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        user = User(username='test',
                    password_hash=hashed_password,
                    password_salt=salt)
        self.session.add(user)
        self.session.flush()

        response = self.app.post_json(
            '/login',
            {'username': 'test',
             'password': 'test123'})

        self.assertEqual(response.status_code, 200)
