"""
User models
"""
from google.appengine.ext import ndb

from app.models import BaseModel


class User(BaseModel):
    """
    User model. user_id mirrors the field provided when a user signs in with the
    Users API provided with App Engine.
    """
    user_id = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()

    @classmethod
    def build_key(cls, user_id):
        """ Build and return a key for an entity. """
        if not user_id:
            raise ValueError("user_id is required")

        return ndb.Key(cls, user_id)

    @classmethod
    def get_users(cls, limit=None):
        """ Gets all User entities. A numerical limit may be passed in. """
        if limit and not isinstance(limit, int):
            raise ValueError("Limit must be an integer")

        return cls.query().fetch(limit=limit)

    @classmethod
    def get_by_user_id(cls, user_id):
        """ Look up users by their user_id. """
        if not user_id:
            raise ValueError("user_id must be provided")

        return cls.build_key(user_id).get()
