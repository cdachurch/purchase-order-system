"""
User views
"""
from flask import Blueprint, redirect, request
from app.views import render_po_template
from app.domain.user import get_current_user
from app.workflow.user import get_or_create_user, get_log_in_out_links_and_user

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/new/")
def new_user():
    context = {}

    # Add the login/out links and the user info
    context.update(get_log_in_out_links_and_user())

    if context["in_datastore"]:
        # Not making someone new, redirect back home
        redirect("/")
    else:
        context["new_user"] = True

    return render_po_template("user.html", **context)


@bp.post("/new/")
def new_user_post():
    name = request.form.get("name")
    email = request.form.get("email")
    users_user = get_current_user()

    # Acknowledging that it will return something, but have no use for it
    _ = get_or_create_user(name, email, users_user["user_id"])

    return redirect("/")
