"""
settings.py Documentation
"""
import os

STATIC_VERSION_NUMBER = 1

SERVER_ADDRESS = "http://po.cdac.ca/"
if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    SERVER_ADDRESS = "http://localhost:8080/"

APPROVAL_ADMINS = [
    "gdholtslander@cdac.ca",
    "gholtslander@cdac.ca",
]
