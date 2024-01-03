"""
User models
"""
from google.cloud import ndb

from app.models import BaseModel


class User(BaseModel):
    """
    User model. user_id mirrors the field provided when a user signs in with the
    Users API provided with App Engine.

    N.B. This model is kind of cruft now, but I don't want to delete it yet.
    It isn't really used for anything (certainly not anymore), which is perhaps too bad.
    Perhaps the last thing it was useful for was a way to hang onto an email address
    that didn't include "@cdac.ca"...  If we had a "superadmin" area we may find it useful to
    have the list of all users who have signed in and when they were created and such.
    """

    user_id = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()

    @classmethod
    def build_key(cls, user_id):
        """Build and return a key for an entity."""
        if not user_id:
            raise ValueError("user_id is required")

        return ndb.Key(cls, user_id)

    @classmethod
    def get_users(cls, limit=None):
        """Gets all User entities. A numerical limit may be passed in."""
        if limit and not isinstance(limit, int):
            raise ValueError("Limit must be an integer")

        return cls.query().fetch(limit=limit)

    @classmethod
    def get_by_user_id(cls, user_id):
        """Look up users by their user_id."""
        if not user_id:
            raise ValueError("user_id must be provided")

        return cls.build_key(user_id).get()

    @classmethod
    def get_by_email(cls, email):
        """Look up user by their email"""
        return ndb.Query("User", ndb.FilterNode("email", "=", email)).get()
