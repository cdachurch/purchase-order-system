"""
Workflow methods for users
"""
from app.domain.user import check_and_return_user, create_user, get_log_links
from app.models.user import User


def get_or_create_user(name, email, user_id):
    """
    Gets the user from the datastore, or creates them (with a domain method)
     if they don't exist
    """
    if not name:
        raise ValueError("name is required")
    if not email:
        raise ValueError("email is required")
    if not user_id:
        raise ValueError("user_id is required")

    key = User.build_key(user_id)

    user = key.get()

    if not user:
        user = create_user(name, email, user_id, key=key)

    return user


def get_log_in_out_links_and_user():
    logout_url, login_url = get_log_links()
    user, is_admin, is_finance_admin = check_and_return_user()

    return {
        "user": user,
        "login": login_url,
        "logout": logout_url,
        "user_is_admin": is_admin,
        "user_is_finance_admin": is_finance_admin,
    }
