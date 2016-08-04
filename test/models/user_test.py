"""
User model tests.
"""
from google.appengine.ext import ndb

from app.domain.user import create_user
from app.models.user import User
from test.fixtures.appengine import GaeTestCase


class UserModelTests(GaeTestCase):
    def setUp(self):
        super(UserModelTests, self).setUp()
        self.name = "Testing"
        self.email = "testing@rocks.com"
        self.user_id = "123456789"
        self.name2 = "Testing2"
        self.email2 = "testing@muchrocks.com"
        self.user_id2 = "987654321"
        self.user2 = create_user(self.name2, self.email2, self.user_id2)

    def test_build_key_requires_user_id(self):
        with self.assertRaises(ValueError):
            User.build_key(None)

    def test_build_key_returns_key(self):
        key = User.build_key(self.user_id)
        self.assertIsInstance(key, ndb.Key)
        self.assertEqual(self.user_id, key.id())

    def test_get_all_users_returns_correct_number_of_users(self):
        users = User.get_users()
        self.assertEqual(1, len(users))
        # Create a user, try it again.
        create_user(self.name, self.email, self.user_id)
        users = User.get_users()
        self.assertEqual(2, len(users))

    def test_get_all_users_with_limit_returns_correct_number_of_users(self):
        create_user(self.name, self.email, self.user_id)
        users = User.get_users(1)
        self.assertEqual(1, len(users))

    def test_get_all_users_limit_must_be_int(self):
        with self.assertRaises(ValueError):
            User.get_users('will not work')

    def test_lookup_user_by_id_requires_user_id(self):
        with self.assertRaises(ValueError):
            User.get_by_user_id(None)

    def test_lookup_user_by_id_returns_correct_user(self):
        found_user = User.get_by_user_id(self.user_id2)
        self.assertIsNotNone(found_user)

        self.assertEqual(found_user.email, self.email2)
        self.assertEqual(found_user.name, self.name2)

    def test_lookup_user_by_id_returns_empty_list(self):
        # Hasn't been created yet, shouldn't return any.
        not_found = User.get_by_user_id(self.user_id)
        self.assertEqual(None, not_found)
