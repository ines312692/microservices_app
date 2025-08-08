import os
import unittest

from users_service.fake.db import dump_users, get_all_users, get_user_by_id


class Test(unittest.TestCase):

    def setUp(self):
        self.users = [
            {
                'id': 1,
                'username': 'admin',
                'email': 'admin@baran.com',
                'full_name': 'Admin Admin',
                'user_type': 'admin',
                'hashed_password': ('$2b$12$16kNu5IW80k1Tw7xz2H3iOCsz0'
                                    '.oMZ7q5OSGa/OIfOae0WGFe8aI2'),
                'created_by': 1
            }

        ]
        self.db = '/tmp/users_service.json'
        dump_users(self.users, self.db)

    def test_get_all_users_are_identical(self):
        users = get_all_users(self.db)
        for user_in_db in users:
            user = user_in_db.dict()
            for column, value in user.items():
                _user = list(
                    filter(lambda u: u['id'] == user['id'], self.users)
                )[0]
                self.assertTrue(_user[column] == value)

    def test_get_user_by_id(self):
        _user = self.users[0]
        pk = _user['id']
        user_in_db = get_user_by_id(pk)
        user = user_in_db.dict()
        for column, value in user.items():
            self.assertEquals(value, _user[column])

    def tearDown(self):
        os.remove(self.db)


unittest.main(verbosity=2)
