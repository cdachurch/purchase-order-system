"""
Interacting with Basecamp todos
"""

import logging
import requests

from app.basecamp.auth import refresh_access_token
from app.domain.user import get_current_ndb_user
import settings


def create_todo_item(todo_url, token, content, description):
    """Creates a todo item in Basecamp and returns its id to be looked up later"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "content": content,
        "description": description,
        "assignee_ids": settings.APPROVAL_ADMINS_BASECAMP_IDS,
        "notify": True,
    }

    response = requests.post(todo_url, headers=headers, json=data).json()
    if "error" in response and response["error"].startswith(
        "OAuth token expired (old age)"
    ):
        user = get_current_ndb_user()
        token = refresh_access_token(user)
        # Try the request again with the new token
        return create_todo_item(todo_url, token, content, description)

    if "id" not in response:
        raise ValueError("Failed to create todo item")

    return response["url"]


def update_todo_item(todo_url, token, content, description, assignee_ids):
    """Updates a todo item in Basecamp"""
    if not token:
        # If the caller didn't pass a token, don't try updating the todo. This person
        # needs to connect to Basecamp, it seems!
        return
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "content": content,
        "description": description,
        "assignee_ids": assignee_ids,
        "notify": True,
        "completed": False,
    }

    response = requests.put(todo_url, headers=headers, json=data)
    res_json = response.json()
    if "error" in res_json and res_json["error"].startswith(
        "OAuth token expired (old age)"
    ):
        logging.info("token expired, refreshing...")
        user = get_current_ndb_user()
        token = refresh_access_token(user)
        # Try the request again with the new token
        return update_todo_item(todo_url, token, content, description, assignee_ids)

    if response.status_code != 200:
        raise ValueError("Failed to update todo item")


def complete_todo_item(todo_url, token):
    """Marks a todo item as done in Basecamp"""
    if not token:
        # If the caller didn't pass a token, don't try updating the todo. This person
        # needs to connect to Basecamp, it seems!
        return
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    todo_url = todo_url.replace(".json", "/completion.json")
    response = requests.post(todo_url, headers=headers)
    # Note, I don't think this endpoint returns JSON, so I don't know if we can refresh
    # the access token if this fails ... BUT, theoretically, this should only ever be called
    # after updating a todo item, which _can_ refresh the token. I guess this is just
    # a note for future me: if you start calling this function from somewhere by itself,
    # you may have to worry about figuring this out :D

    if response.status_code != 204:
        raise ValueError("Failed to complete todo item")
