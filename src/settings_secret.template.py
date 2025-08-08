"""
settings_secret.template.py

This file should be copied and renamed settings_secret.py, which is not checked into version control.
These values can all be fetched from Secret Manager, here:
https://console.cloud.google.com/security/secret-manager?project=cdac-purchaseorder
and
https://console.cloud.google.com/security/secret-manager?project=cdac-demo-purchaseorder
"""

CLIENT_CONFIG = ""
CLIENT_CONFIG_PROD = ""

SESSION_SECRET_DEMO = ""
SESSION_SECRET_PROD = ""

SENDGRID_KEY = ""

# Get these from https://launchpad.37signals.com/integrations/17272
BASECAMP_CLIENT_ID = ""
BASECAMP_CLIENT_SECRET = ""
