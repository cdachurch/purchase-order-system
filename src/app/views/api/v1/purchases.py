"""
Purchases api endpoints
"""
from app.views.api.v1 import BaseApiMixin, AddressPurchaseOrderMixin, API_CONSTANTS
from app.domain.purchase import create_purchase_order, get_purchase_order_entity


class PurchaseCreateApi(BaseApiMixin):
    """
    API for creating purchase orders
    """
    def post(self):
        """ Post routines """
        post_body = self.request.POST
        get_params = self.request.GET
        # required attributes
        try:
            api_user = get_params[API_CONSTANTS.API_USER]
            api_key = get_params[API_CONSTANTS.API_KEY]
            purchaser = post_body[API_CONSTANTS.USERNAME]
            product = post_body[API_CONSTANTS.PRODUCT]
            supplier = post_body[API_CONSTANTS.SUPPLIER]
            price = post_body[API_CONSTANTS.PRICE]
        except KeyError as ke:
            self.return_error_with_code(400, "A required field is missing: %s" % ke.message)

        if not self.validate_api_user_and_key(api_user, api_key):
            self.return_error_with_code(403, "You are not authorized to access this URL")
            return

        try:
            # if we get here, all would appear to be well; create the purchase order
            new_po_id = create_purchase_order(purchaser, supplier, product, price)

            return_dict = {
                "data": {
                    "po_id": new_po_id
                }
            }

            self.return_data_with_code(201, return_dict)
        except ValueError as ve:
            self.return_error_with_code(400, "There was an error with creation: %s" % ve.message)


class PurchaseAcceptApi(BaseApiMixin, AddressPurchaseOrderMixin):
    """
    API for accepting purchase orders
    """
    def get(self, po_id):
        if not po_id:
            self.return_error_with_code(400, "You didn't get here the right way")
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            po_entity.is_approved = True
            po_entity.put()
            self.send_email(po_entity.purchaser, API_CONSTANTS.ACCEPTED, po_entity)
            self.return_data_with_code(200)


class PurchaseDenyApi(BaseApiMixin, AddressPurchaseOrderMixin):
    """
    API for denying purchase orders
    """
    def get(self, po_id):
        if not po_id:
            self.return_error_with_code(400, "You didn't get here the right way")
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            po_entity.is_denied = True
            po_entity.put()
            self.send_email(po_entity.purchaser, API_CONSTANTS.DENIED, po_entity)
            self.return_data_with_code(200)
