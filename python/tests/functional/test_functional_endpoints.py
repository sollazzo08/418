import datetime
from flask.wrappers import Response
import unittest

from tests.functional.functional_test_client import FunctionalTestClient
from ratemydorm.sql.table_types import UserProfile

profile_keys = UserProfile.__annotations__.keys()

USER_ID = 2
DORM_ID = 999999
TIMESTAMP = datetime.datetime.now()
RATING = 1
REVIEW_TEXT = 'I LOVED HATED ENJOYED DESPISED SOMETHINGED this dorm'


class TestEndpoints(FunctionalTestClient):
    def setUp(self):
        self._data =  {
            'user_id': USER_ID,
            'dorm_id': DORM_ID,
            'timestamp': TIMESTAMP,
            'rating': RATING,
            'review_text': REVIEW_TEXT
        }
        super().setUp()

    def test_get_user_profile(self):
        user_id = 2
        query = {'user_id': user_id}
        result = self.get('/user/profile', query)

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get('payload'), dict)
        self.assertCountEqual(profile_keys, result.get('payload').get('user').keys())

    def test_add_review_fails_with_missing_input(self):
        data = self._data
        data['rating'] = None
        result = self.post('/dorms/review', data=data)
        response: Response = self._response
        self.assertEqual(400, response.status_code)
        self.assertIn('Not all fields are filled out', result.get('message'))

    def test_add_review_fails_with_invalid_dorm_id(self):
        data = self._data
        result = self.post('/dorms/review', data=data)
        response: Response = self._response
        self.assertEqual(400, response.status_code)
        self.assertIn('foreign key constraint fails', result.get('message'))

    def test_add_review_fails_with_invalid_user_id(self):
        data = self._data
        data['user_id'] = 9999909
        data['dorm_id'] = 1

        result = self.post('/dorms/review', data=data)
        response: Response = self._response
        self.assertEqual(400, response.status_code)
        self.assertIn('foreign key constraint fails', result.get('message'))

    @unittest.skip
    def test_adding_review(self):
        data = self._data
        data['dorm_id'] = 2

        result = self.post('/dorms/review', data=data)
        response: Response = self._response
        self.assertEqual(response.status_code, 200)

    def test_get_profile_history(self):
        user_id = 18
        query = {'user_id': user_id}
        expected_review = 'I LOVED HATED ENJOYED DESPISED SOMETHINGED this dorm'
        result = self.get('/user/profile', query)
        self.assertEqual(expected_review, result['payload']['reviews'][0]['review_text'])
        self.assertEqual(2, len(result['payload']['reviews']))
        self.assertEqual(2, len(result['payload']['images']))

    def test_get_profile_history_missing_user(self):
        user_id = -1
        query = {'user_id': user_id}

        result = self.get('/user/profile', query)
        self.assertEqual({}, result.get('payload'))