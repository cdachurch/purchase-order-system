"""
settings.py Documentation
"""
import os

# CLIENT_CONFIG is the contents of the file you can download from "Client ID for Web application" in
# the Google Cloud console
from settings_secret import CLIENT_CONFIG, SESSION_SECRET

# TODO: Update to prod client id eventually
OAUTH_CLIENT_ID = (
    "493242818739-15dviusnrma4om6bsk4ar48easltjdo2.apps.googleusercontent.com"
)
ENVIRONMENT = "PROD"
SERVER_ADDRESS = "https://po.cdac.ca/"
if (
    "APPLICATION_ID" in os.environ
    and os.environ["APPLICATION_ID"].find("cdac-demo-purchaseorder") >= 0
):
    SERVER_ADDRESS = "https://cdac-demo-purchaseorder.appspot.com/"
    ENVIRONMENT = "DEMO"
    OAUTH_CLIENT_ID = (
        "493242818739-15dviusnrma4om6bsk4ar48easltjdo2.apps.googleusercontent.com"
    )
if "SERVER_SOFTWARE" in os.environ and os.environ["SERVER_SOFTWARE"].startswith(
    "Development"
):
    SERVER_ADDRESS = "http://localhost:5000/"
    ENVIRONMENT = "LOCAL"
    OAUTH_CLIENT_ID = (
        "493242818739-15dviusnrma4om6bsk4ar48easltjdo2.apps.googleusercontent.com"
    )

APPROVAL_ADMINS = [
    "gdholtslander",
    "gholtslander",
    "smyhre",
    "gdholtslander@cdac.ca",
    "gholtslander@cdac.ca",
    "smyhre@cdac.ca",
]

FINANCE_ADMINS = [
    "dwiebe",
    "gdholtslander",
    "dwiebe@cdac.ca",
    "gdholtslander@cdac.ca",
    "test@example.com",
]

CAN_SEE_ALL_POS = (
    APPROVAL_ADMINS
    + FINANCE_ADMINS
    + [
        "jheindle",
        "rhoult",
        "rsmith",
    ]
)


def is_approval_admin(email):
    """Email addresses that can approve purchase orders"""
    return email in APPROVAL_ADMINS


def is_finance_admin(email):
    """Email addresses that can do finance related tasks to POs (cancel them, mainly)"""
    return email in FINANCE_ADMINS


POS_FOR_PURCHASER_MEMCACHE_KEY = "all-pos-for-{}"
ALL_POS_ORDERED_MEMCACHE_KEY = "all-pos-for-order-{}"


def is_devappserver():
    return os.environ.get("GAE_APPLICATION") == "local"
