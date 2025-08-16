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
import requests

from app.domain.user import get_current_ndb_user


authorization_url = "https://launchpad.37signals.com/authorization.json"
projects_url = "https://3.basecampapi.com/{account_id}/projects.json"


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

    todoset_url = ""
    for item in projects_resp[0]["dock"]:
        if item["name"] == "todoset":
            todoset_url = item["url"]
            break

    if todoset_url == "":
        raise ValueError("todoset project not found in Basecamp projects")

    todoset_resp = requests.get(
        todoset_url, headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    todolists_resp = requests.get(
        todoset_resp["todolists_url"],
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    todos_url = ""
    for todolist in todolists_resp:
        if todolist["name"] == "Purchase Orders":
            todos_url = todolist["todos_url"]
            break

    if todos_url == "":
        raise ValueError("Purchase Orders todo list not found in todoset")

    user = get_current_ndb_user()
    user.basecamp_refresh_token = refresh_token
    user.basecamp_access_token = access_token
    user.basecamp_todos_url = todos_url
    user.put()
