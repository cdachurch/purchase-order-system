"""
API base view
"""
import json

from app.utility.mailer import send_message


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
        <h2>Purchase order approved!</h2>

        <p>Your purchase order number is #{ppoid}. Here's what this purchase order covers:</p>

        <ul>
            <li>Supplier: {supplier}</li>
            <li>Product: {product}</li>
            <li>Price: ${:,.2f}</li>
        </ul>

        <p>Have a nice day!</p>
    """

    DENIED_SUBJECT = "Your purchase order was denied"
    DENIED_EMAIL_HTML = """
        <h2>Purchase order #{ppoid} denied!</h2>

        <p>Your purchase order #{ppoid} has been denied. Here's what was on it:</p>

        <ul>
            <li>Supplier: {supplier}</li>
            <li>Product: {product}</li>
            <li>Price: ${:,.2f}</li>
        </ul>

        <p>Contact administration for an explanation - please do not reply to this email.</p>
    """
