"""
Routes relating to authentication I guess
"""
from flask import Blueprint, session, request, redirect, url_for
from google.cloud import ndb

import requests

import google_auth_oauthlib.flow
from app.models.user import User

import settings

client = ndb.Client()

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login")
def oauth_login():
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        settings.CLIENT_CONFIG,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ],
    )

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = "https://127.0.0.1:5000/auth/oauth2callback"

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@bp.route("/oauth2callback")
def oauth_callback():
    state = session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        settings.CLIENT_CONFIG,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ],
        state=state,
    )
    flow.redirect_uri = url_for("auth.oauth_callback", _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials

    user_info = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": "Bearer " + credentials.token},
    ).json()

    email = user_info["email"]

    # cdac.ca emails only
    split_email = email.split("@")
    if split_email[1] != "cdac.ca":
        return redirect(url_for("index"))

    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    # https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
    session["email"] = email
    session["user_id"] = user_info["sub"]
    session["name"] = user_info["given_name"]
    # "{'sub': '108580537957365284310', 'name': 'Graham Holtslander', 'given_name': 'Graham',
    # 'family_name': 'Holtslander', 'picture':
    # 'https://lh3.googleusercontent.com/a/ACg8ocKF9QIr4l5aD6UsDaickJTBXKFN_NjlXnDJv0UOU2DB=s96-c',
    # 'email': 'gdholtslander@cdac.ca', 'email_verified': True, 'locale': 'en', 'hd': 'cdac.ca'}

    with client.context():
        user = User.get_by_email(split_email[0])
        if user is None:
            return redirect(url_for("user.new_user"))

    return redirect(url_for("index"))


@bp.route("/logout")
def logout():
    del session["email"]
    del session["name"]
    del session["user_id"]

    return redirect("/")
