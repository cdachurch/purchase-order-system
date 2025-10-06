"""
Newly authed users flow through here
"""

"""
Example response:
{
	"expires_at": "2025-08-22T04:41:46.000Z",
	"identity": {
		"id": 1234567,
		"email_address": "",
		"first_name": "Graham",
		"last_name": "H"
	},
	"accounts": [
		{
			"id": 123456,
			"name": "CircleYXE",
			"product": "bc3",
			"href": "https://3.basecampapi.com/123456",
			"app_href": "https://3.basecamp.com/123456",
			"hidden": false
		},
        {
            ...
        }
	]
}
"""
import logging
import requests

import settings

from app.domain.user import get_current_ndb_user


authorization_url = "https://launchpad.37signals.com/authorization.json"
projects_url = "https://3.basecampapi.com/{account_id}/projects.json"
my_personal_info = "https://3.basecampapi.com/{account_id}/my/profile.json"
refresh_token_url = "https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}"


def new_user_work(token):
    """
    Do several things for a brand new user, such as fetching their account id and various project
    and other ids
    """
    access_token = token["access_token"]
    refresh_token = token["refresh_token"]

    auth_resp = requests.get(
        authorization_url, headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    circle_project_id = 0
    logging.info(f"BC auth response: {auth_resp}")
    for account in auth_resp["accounts"]:
        if account["name"] == "CircleYXE":
            circle_project_id = account["id"]
            break

    if circle_project_id == 0:
        raise ValueError("CircleYXE account not found in Basecamp accounts")

    # Get the projects the user has access to, (hopefully all of the ones that we need!)
    projects_resp = requests.get(
        projects_url.format(account_id=circle_project_id),
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    logging.info(f"BC projects response: {projects_resp}")
    todoset_url = ""
    for project in projects_resp:
        if project["name"] != "PO Connection":
            continue
        for item in project["dock"]:
            if item["name"] == "todoset":
                todoset_url = item["url"]
                break

    if todoset_url == "":
        raise ValueError("todoset project not found in Basecamp projects")

    todoset_resp = requests.get(
        todoset_url, headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    logging.info(f"BC todoset response: {todoset_resp}")

    todolists_resp = requests.get(
        todoset_resp["todolists_url"],
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    logging.info(f"BC todolists response: {todolists_resp}")
    todos_url = ""
    for todolist in todolists_resp:
        if todolist["name"] == "Purchase Orders":
            todos_url = todolist["todos_url"]
            break

    if todos_url == "":
        raise ValueError("Purchase Orders todo list not found in todoset")

    my_info_resp = requests.get(
        my_personal_info.format(account_id=circle_project_id),
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    logging.info(f"BC my info response: {my_info_resp}")
    assignee_id = my_info_resp["id"]

    user = get_current_ndb_user()
    user.basecamp_refresh_token = refresh_token
    user.basecamp_access_token = access_token
    user.basecamp_todos_url = todos_url
    user.basecamp_assignee_id = assignee_id
    user.put()


def refresh_access_token(user):
    """
    Refresh the Basecamp access token for the given user.
    """
    refresh_token = user.basecamp_refresh_token
    if not refresh_token:
        raise ValueError("No refresh token available")

    # Make a request to refresh the access token
    response = requests.post(
        refresh_token_url.format(
            refresh_token=refresh_token,
            client_id=settings.BASECAMP_CLIENT_ID,
            client_secret=settings.BASECAMP_CLIENT_SECRET,
        )
    ).json()

    if "access_token" not in response:
        raise ValueError("Failed to refresh access token")
    print(response)

    user.basecamp_access_token = response["access_token"]
    user.put()

    return response["access_token"]
