import unittest
from app import create_app, db


class FlaskJwtAuthTest(unittest.TestCase):
    '''
    '''

    def setUp(self):
        '''

        '''
        self.app = create_app()
        self.client = self.app.test_client

    def test_route(self):
        '''
        '''
        # res = self.client().post('/bucketlists/', data=self.bucketlist)
        # self.assertEqual(res.status_code, 201)
        # self.assertIn('Go to Borabora', str(res.data))

    def tearDown(self):
        '''
        '''
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
