"""
settings.py Documentation
"""

import os

# CLIENT_CONFIG is the contents of the file you can download from "Client ID for Web application" in
# the Google Cloud console
from settings_secret import (
    CLIENT_CONFIG_DEMO,
    CLIENT_CONFIG_PROD,
    SESSION_SECRET_DEMO,
    SESSION_SECRET_PROD,
    BASECAMP_CLIENT_ID_PROD,
    BASECAMP_CLIENT_SECRET_PROD,
    BASECAMP_CLIENT_ID_DEMO,
    BASECAMP_CLIENT_SECRET_DEMO,
    BASECAMP_CLIENT_ID_LOCAL,
    BASECAMP_CLIENT_SECRET_LOCAL,
    BASECAMP_CAMPFIRE_URL,
    DELETE_LINES_URL,
)

OAUTH_CLIENT_ID = (
    "1010082857204-kg196opkkbfpt0ppkf14qg6pvr6hhcep.apps.googleusercontent.com"
)
ENVIRONMENT = "PROD"
SERVER_ADDRESS = "https://po.cdac.ca/"
CLIENT_CONFIG = CLIENT_CONFIG_PROD
SESSION_SECRET = SESSION_SECRET_PROD
BASECAMP_CLIENT_ID = BASECAMP_CLIENT_ID_PROD
BASECAMP_CLIENT_SECRET = BASECAMP_CLIENT_SECRET_PROD

if (
    "GAE_APPLICATION" in os.environ
    and os.environ["GAE_APPLICATION"].find("cdac-demo-purchaseorder") >= 0
):
    SERVER_ADDRESS = "https://cdac-demo-purchaseorder.appspot.com/"
    ENVIRONMENT = "DEMO"
    OAUTH_CLIENT_ID = (
        "493242818739-15dviusnrma4om6bsk4ar48easltjdo2.apps.googleusercontent.com"
    )
    CLIENT_CONFIG = CLIENT_CONFIG_DEMO
    SESSION_SECRET = SESSION_SECRET_DEMO
    BASECAMP_CLIENT_ID = BASECAMP_CLIENT_ID_DEMO
    BASECAMP_CLIENT_SECRET = BASECAMP_CLIENT_SECRET_DEMO
if "SERVER_SOFTWARE" in os.environ and os.environ["SERVER_SOFTWARE"].startswith(
    "Development"
):
    SERVER_ADDRESS = "https://localhost:5000/"
    ENVIRONMENT = "LOCAL"
    OAUTH_CLIENT_ID = (
        "493242818739-15dviusnrma4om6bsk4ar48easltjdo2.apps.googleusercontent.com"
    )
    CLIENT_CONFIG = CLIENT_CONFIG_DEMO
    SESSION_SECRET = SESSION_SECRET_DEMO
    BASECAMP_CLIENT_ID = BASECAMP_CLIENT_ID_LOCAL
    BASECAMP_CLIENT_SECRET = BASECAMP_CLIENT_SECRET_LOCAL

OAUTH_REDIRECT_URI = "%sauth/oauth2callback" % (SERVER_ADDRESS)
BC_OAUTH_REDIRECT_URI = "%s/bccallback" % (SERVER_ADDRESS)

APPROVAL_ADMINS = [
    # "gdholtslander@cdac.ca",
    # "gholtslander@cdac.ca",
    "smyhre@cdac.ca",
    "cbayles@cdac.ca",
]

APPROVAL_ADMINS_BASECAMP_IDS = [
    26436056,  # Sherry
    26594357,  # Cindy
    # 48801289,  # Graham
    # 34740541,  # Gordon
]
FINANCE_ADMINS_BASECAMP_IDS = [
    26594358,  # Deseree
    # 48801289,  # Graham
]

FINANCE_ADMINS = [
    "dwiebe@cdac.ca",
    # "gdholtslander@cdac.ca",
]


def is_approval_admin(email):
    """Email addresses that can approve purchase orders"""
    return email in APPROVAL_ADMINS


def is_finance_admin(email):
    """Email addresses that can do finance related tasks to POs (cancel them, mainly)"""
    return email in FINANCE_ADMINS
