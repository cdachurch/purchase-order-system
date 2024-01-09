"""
Domain functions for users
"""
from google.cloud import ndb
from flask import session
import settings
from app.models.user import User

client = ndb.Client()


def check_and_return_user():
    """
    Returns a Users.user object, an ndb_user, and whether or not they exist in datastore
    """
    user = get_current_user()
    is_finance_admin = False
    is_approval_admin = False

    if user:
        is_approval_admin = settings.is_approval_admin(user["email"])
        is_finance_admin = settings.is_finance_admin(user["email"])

    return user, is_approval_admin, is_finance_admin


def create_user(name, email, user_id, key=None):
    """
    Takes an optional key and a name, email, and user_id to create a user
    If key is not provided, one will be created from the user_id
    """
    if not name:
        raise ValueError("name is required")
    if not email:
        raise ValueError("email is required")
    if not email.find("@"):
        email += "@cdac.ca"
    if not user_id:
        raise ValueError("user_id is required")
    if not key:
        # Make our own dang key!
        key = User.build_key(user_id)

    kwargs = {"name": name, "email": email, "user_id": user_id}
    user = User(key=key, **kwargs)

    user.put()

    return user


def get_current_user():
    """Get the current user from the session"""
    if not all(["email" in session, "user_id" in session, "name" in session]):
        return None

    user = {
        "email": session["email"],
        "user_id": session["user_id"],
        "name": session["name"],
    }
    return user


def get_log_links():
    """Get the log(in|out) links for a user"""
    return "/auth/logout", "/auth/login"
