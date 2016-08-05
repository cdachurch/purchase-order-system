"""
Purchases api endpoints
"""
from app.views.api.v1 import BaseApiMixin, AddressPurchaseOrderMixin, API_CONSTANTS
from app.domain.purchase import approve_purchase_order, cancel_purchase_order, create_interim_purchase_order, \
                                create_purchase_order, deny_purchase_order, get_all_purchase_orders, \
                                get_purchase_order_entity, get_purchase_order_to_dict, \
                                get_purchase_orders_by_purchaser
from app.domain.user import check_and_return_user


class CreateInterimPurchaseApi(BaseApiMixin):
    """
    API to create interim purchase orders
    """
    def post(self):
        po_entity = create_interim_purchase_order()
        return_dict = {
            "data": {
                "po_id": po_entity.po_id,
                "pretty_po_id": po_entity.pretty_po_id
            }
        }
        self.return_data_with_code(200, return_dict)


class PurchaseGetApi(BaseApiMixin):
    """
    API for getting purchase orders
    """
    def get(self):
        get_params = self.request.GET

        po_id = get_params.get(API_CONSTANTS.PO_ID)
        email = get_params.get(API_CONSTANTS.EMAIL)
        if po_id:
            po_entity_dict = get_purchase_order_to_dict(po_id=po_id)
            return self.return_data_with_code(200, po_entity_dict)
        else:
            if email:
                po_entitys = get_purchase_orders_by_purchaser(email)
            else:
                po_entitys = get_all_purchase_orders(order_direction="DESC")
            return_dict = {
                "data": []
            }
            for po_entity in po_entitys:
                return_dict["data"].append(po_entity.to_dict())
            return self.return_data_with_code(200, return_dict)


class PurchaseCreateApi(BaseApiMixin):
    """
    API for creating purchase orders
    """
    def post(self):
        """ Post routes """
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
            account_code = post_body.get(API_CONSTANTS.ACCOUNT_CODE)
        except KeyError as ke:
            self.return_error_with_code(400, "A required field is missing: %s" % ke.message)

        if not self.validate_api_user_and_key(api_user, api_key):
            self.return_error_with_code(403, "You are not authorized to access this URL")
            return

        try:
            # if we get here, all would appear to be well; create the purchase order
            new_po_id = create_purchase_order(purchaser, supplier, product, price, account_code=account_code)

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
            _, approver, _, _, _ = check_and_return_user()
            approve_purchase_order(po_entity, approver)
            self.send_email(po_entity.purchaser, API_CONSTANTS.ACCEPTED, po_entity)
            self.return_data_with_code(200)


class PurchaseCancelApi(BaseApiMixin):
    """
    API for cancelling purchase orders
    """
    def get(self, po_id):
        if not po_id:
            self.return_error_with_code(400, "You didn't get here the right way")
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            cancel_purchase_order(po_entity)
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
            deny_purchase_order(po_entity)
            self.send_email(po_entity.purchaser, API_CONSTANTS.DENIED, po_entity)
            self.return_data_with_code(200)


class PurchaseInvoiceApi(BaseApiMixin):
    """
    API for marking purchase orders as "invoiced"
    """
    def get(self, po_id):
        if not po_id:
            self.return_error_with_code(400, "You didn't get here the right way")
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            # flip that bit
            po_entity.is_invoiced = not po_entity.is_invoiced
            po_entity.put()
            self.return_data_with_code(200)
