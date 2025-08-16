"""
Interacting with Basecamp todos
"""

# Base url for interacting with the Purchase Orders "basecamp" or whatever
import requests

import settings


def create_todo_item(todo_url, token, content, description):
    """Creates a todo item in Basecamp and returns its id to be looked up later"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "content": content,
        "description": description,
        # FIXME: Why didn't this work?
        "assignee_ids": settings.APPROVAL_ADMINS_BASECAMP_IDS,
        "notify": True,
    }
    response = requests.post(todo_url, headers=headers, json=data).json()
    if "id" not in response:
        raise ValueError("Failed to create todo item")

    return response["url"]


def update_todo_item(todo_url, token, content, description):
    """Updates a todo item in Basecamp"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "content": content,
        "description": description,
        # TODO: Assign to the PO creator and the finance admins
        "assignee_ids": settings.APPROVAL_ADMINS_BASECAMP_IDS,
        "notify": True,
    }

    resp = requests.put(todo_url, headers=headers, json=data)
    if resp.status_code != 200:
        raise ValueError("Failed to update todo item")
