"""
Interacting with Basecamp todos
"""

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


def update_todo_item(todo_url, token, content, description, assignee_id):
    """Updates a todo item in Basecamp"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "content": content,
        "description": description,
        "assignee_ids": [assignee_id] + settings.FINANCE_ADMINS_BASECAMP_IDS,
        "notify": True,
        "completed": False,
    }

    response = requests.put(todo_url, headers=headers, json=data)
    if "error" in response and response["error"].startswith(
        "OAuth token expired (old age)"
    ):
        user = get_current_ndb_user()
        token = refresh_access_token(user)
        # Try the request again with the new token
        return update_todo_item(todo_url, token, content, description)

    if response.status_code != 200:
        raise ValueError("Failed to update todo item")
