"""
API base view
"""
import json

from webapp2 import RequestHandler

from app.utility.mailer import send_message

class AcceptedUsers(object):
    API_USERS = [
        "gs"
    ]

    API_KEYS = {
        "gs": "861d88e2-bf68-41af-bbe7-617be8b98114"
    }


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


class BaseApiMixin(RequestHandler):

    def validate_api_user_and_key(self, api_user, api_key):
        return api_user in AcceptedUsers.API_USERS and AcceptedUsers.API_KEYS[api_user] == api_key

    def return_error_with_code(self, status_code, message):
        self.response.headers['Content-Type'] = API_CONSTANTS.RETURN_CONTENT_TYPE
        self.response.set_status(status_code)
        self.response.out.write(json.dumps({
            "status": status_code,
            "error": message
            }))

    def return_data_with_code(self, status_code, data_dict=None):
        if data_dict and not isinstance(data_dict, dict):
            raise ValueError("data_dict must be a dictionary")
        if not data_dict:
            data_dict = {}
        self.response.headers['Content-Type'] = API_CONSTANTS.RETURN_CONTENT_TYPE
        self.response.set_status(status_code)
        data_dict["status"] = status_code
        self.response.out.write(json.dumps(data_dict))


class AddressPurchaseOrderMixin(object):

    def send_email(self, to, how, po_entity):
        supplier = po_entity.supplier
        product = po_entity.product
        price = po_entity.price
        pretty_po_id = po_entity.pretty_po_id
        if how == API_CONSTANTS.ACCEPTED:
            send_message(to, API_CONSTANTS.ACCEPTED_SUBJECT,
                         html=API_CONSTANTS.ACCEPTED_EMAIL_HTML.format(price, ppoid=str(pretty_po_id).zfill(4),
                                 supplier=supplier, product=product))
        elif how == API_CONSTANTS.DENIED:
            send_message(to, API_CONSTANTS.DENIED_SUBJECT, 
                         html=API_CONSTANTS.DENIED_EMAIL_HTML.format(price, ppoid=str(pretty_po_id).zfill(4),
                                 supplier=supplier, product=product))

