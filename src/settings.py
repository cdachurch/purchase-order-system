"""
settings.py Documentation
"""
import os

STATIC_VERSION_NUMBER = 1

ENVIRONMENT = "PROD"
SERVER_ADDRESS = "https://po.cdac.ca/"
if os.environ['APPLICATION_ID'].find("cdac-demo-purchaseorder") >= 0:
    SERVER_ADDRESS = "https://cdac-demo-purchaseorder.appspot.com/"
    ENVIRONMENT = "DEMO"
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Development'):
    SERVER_ADDRESS = "http://localhost:8080/"
    ENVIRONMENT = "LOCAL"

APPROVAL_ADMINS = [
    "gdholtslander",
    "gholtslander",
    # "lkrieg",
    "smyhre",
    "test@example.com"
]

FINANCE_ADMINS = [
    "dwiebe",
    "gdholtslander",
    "test@example.com"
]


def is_approval_admin(email):
    """ Email addresses that can approve purchase orders """
    return email in APPROVAL_ADMINS


def is_finance_admin(email):
    """ Email addresses that can do finance related tasks to POs (cancel them, mainly) """
    return email in FINANCE_ADMINS


POS_FOR_PURCHASER_MEMCACHE_KEY = 'all-pos-for-{}'
ALL_POS_ORDERED_MEMCACHE_KEY = 'all-pos-for-order-{}'
