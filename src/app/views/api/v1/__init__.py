"""
API base view
"""


class AcceptedUsers(object):
    API_USERS = ["gs"]

    API_KEYS = {"gs": "861d88e2-bf68-41af-bbe7-617be8b98114"}


class API_CONSTANTS(object):
    API_USER = "apiUser"
    API_KEY = "apiKey"
    USERNAME = "username"
    EMAIL = "email"
    PRODUCT = "product"
    SUPPLIER = "supplier"
    PRICE = "price"
    ACCEPTED = "accepted"
    DENIED = "denied"
    ACCOUNT_CODE = "accountCode"
    RETURN_CONTENT_TYPE = "application/json"
    PO_ID = "poId"

    ACCEPTED_SUBJECT = "Your purchase order was approved"
    ACCEPTED_EMAIL_HTML = """
        <p>Purchase order <a href="{approval_link}">#{ppoid}</a> was approved</p>
    """

    DENIED_SUBJECT = "Your purchase order was denied"
    DENIED_EMAIL_HTML = """
        <p>Purchase order <a href="{approval_link}">#{ppoid}</a> denied</p>
    """
