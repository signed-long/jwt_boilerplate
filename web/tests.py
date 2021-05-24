import unittest
from app import create_app, db
import json
from app.models import User
from app.utils.helpers import get_id_from_jwt
from os import environ
import time


class FlaskJwtAuthTest(unittest.TestCase):
    def setUp(self):
        '''
        Runs before every method.
        '''
        self.app = create_app()
        self.client = self.app.test_client
        self.auth_header = None

        with self.app.app_context():
            db.create_all()
            db.session.commit()

    def tearDown(self):
        '''
        Runs after every method.
        '''
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        '''
        Tests the registration route.
        '''
        # resister test user
        body = {"email": "testUser@test.ca", "password": "pass"}
        res = register_user(self.client, body)
        self.assertEqual(res.status_code, 201)

        # test invalid requests
        body = {"email": "testUser@test.ca"}
        res = register_user(self.client, body)
        self.assertEqual(res.status_code, 400)

        body = {"password": "pass"}
        res = register_user(self.client, body)
        self.assertEqual(res.status_code, 400)

        body = {"something_else": "idk"}
        res = register_user(self.client, body)
        self.assertEqual(res.status_code, 400)

        body = {}
        res = register_user(self.client, body)
        self.assertEqual(res.status_code, 400)

    def test_login(self):
        '''
        Tests the login route.
        '''
        # register / login
        body = {"email": "testUser@test.ca", "password": "pass"}
        register_res = register_user(self.client, body)
        self.assertEqual(register_res.status_code, 201)
        login_res = login_user(self.client, body)
        data = json.loads(login_res.data.decode())
        self.assertEqual(login_res.status_code, 200)

        # assert we recieve our tokens
        self.assertTrue(data["data"]["access_token"])
        self.assertTrue(data["data"]["refresh_token"])

        # assert these tokens are valid
        with self.app.app_context():
            user_id = User.query.filter_by(email=body["email"]).first().id
        user_id_at = get_id_from_jwt(data["data"]["access_token"],
                                     environ.get("ACCESS_TOKEN_SECRET"))
        user_id_rt = get_id_from_jwt(data["data"]["refresh_token"],
                                     environ.get("REFRESH_TOKEN_SECRET"))
        self.assertTrue(user_id_at == user_id_rt == user_id)

        # test invalid requests
        body = {"email": "NoUser@test.ca", "password": "pass"}
        login_res = login_user(self.client, body)
        self.assertEqual(login_res.status_code, 401)

        body = {"email": "testUser@test.ca", "password": "wrong_pass"}
        login_res = login_user(self.client, body)
        self.assertEqual(login_res.status_code, 401)

        body = {"email": "testUser@test.ca"}
        login_res = login_user(self.client, body)
        self.assertEqual(login_res.status_code, 400)

        body = {"password": "pass"}
        login_res = login_user(self.client, body)
        self.assertEqual(login_res.status_code, 400)

        body = {}
        login_res = login_user(self.client, body)
        self.assertEqual(login_res.status_code, 400)

    def test_get(self):
        '''
        Tests the 'test' route.
        '''
        # register / login
        body = {"email": "testUser@test.ca", "password": "pass"}
        register_res = register_user(self.client, body)
        self.assertEqual(register_res.status_code, 201)
        login_res = login_user(self.client, body)
        data = json.loads(login_res.data.decode())
        self.assertEqual(login_res.status_code, 200)

        # get tokens
        data = json.loads(login_res.data.decode())
        access_token = data["data"]["access_token"]

        # send get request to '/test'
        headers = {"Authorization": "Bearer " + str(access_token)}
        res = self.client().get('/test', headers=headers)
        self.assertEqual(res.status_code, 200)

        # expire token and try again
        time.sleep(6)
        res = self.client().get('/test', headers=headers)
        self.assertEqual(res.status_code, 401)

    def test_refresh(self):
        '''
        Tests the refresh route.
        '''
        # register / login
        body = {"email": "testUser@test.ca", "password": "pass"}
        register_res = register_user(self.client, body)
        self.assertEqual(register_res.status_code, 201)
        login_res = login_user(self.client, body)
        data = json.loads(login_res.data.decode())
        self.assertEqual(login_res.status_code, 200)

        # get tokens
        data = json.loads(login_res.data.decode())
        refresh_token = data["data"]["refresh_token"]
        access_token = data["data"]["access_token"]

        # expire token
        time.sleep(6)
        headers = {"Authorization": "Bearer " + str(access_token)}
        res = self.client().get('/test', headers=headers)
        self.assertEqual(res.status_code, 401)

        # get fresh access token
        body = {"refresh_token": refresh_token}
        res = self.client().get('/refresh', data=json.dumps(body), content_type='application/json')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data.decode())
        access_token = data["data"]["access_token"]

        # test new access token
        headers = {"Authorization": "Bearer " + str(access_token)}
        res = self.client().get('/test', headers=headers)
        self.assertEqual(res.status_code, 200)


def register_user(client, body):
    '''
    Resisters a user.
    '''
    return client().post(
        '/register',
        data=json.dumps(body),
        content_type='application/json',
    )


def login_user(client, body):
    '''
    Logs in a user.
    '''
    return client().post(
        '/login',
        data=json.dumps(body),
        content_type='application/json',
    )


if __name__ == "__main__":
    unittest.main()
