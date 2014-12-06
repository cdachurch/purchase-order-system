"""
Views for purchase orders
"""
import logging

from app.domain.purchase import create_purchase_order, get_purchase_order_to_dict, \
                                get_all_purchase_orders, get_purchase_orders_by_purchaser, \
                                send_admin_email_for_new_po
from app.models.purchaseorder import PurchaseOrder
from app.views import TemplatedView
from app.workflow.user import get_log_in_out_links_and_user

class PurchaseView(TemplatedView):
    def get(self, po_id):
        bread_crumbs = [
            ("Home", self.uri_for('index')),
            ("List purchase orders", self.uri_for("list_purchases")),
            ("View purchase order", None)
        ]

        context = {}

        # Add the login/out links and the user info
        context.update(get_log_in_out_links_and_user())

        try:
            po_dict = get_purchase_order_to_dict(po_id=po_id)
        except ValueError as ve:
            self.render_response("404.html", **context)
            return
        
        context.update(po_dict)
        context["bread_crumbs"] = bread_crumbs

        self.render_response("purchase.html", **context)


class PurchaseListView(TemplatedView):
    def get(self):
        bread_crumbs = [
            ("Home", self.uri_for('index')),
            ("List purchase orders", None)
        ]

        context = {
            # "purchase_orders": get_all_purchase_orders(),
            "bread_crumbs": bread_crumbs
        }

        # Add the login/out links and the user info
        context.update(get_log_in_out_links_and_user())

        self.render_response("purchaseorders.html", **context)


class PurchaseCreateView(TemplatedView):
    def get(self, **context):
        bread_crumbs = [
            ("Home", self.uri_for('index')),
            ("List purchase orders", self.uri_for("list_purchases")),
            ("Create purchase order", None)
        ]
        if not context:
            context = {}
        context["bread_crumbs"] = bread_crumbs
        if not context.get("form", None):
            context["form"] = {}
        # Add the login/out links and the user info
        context.update(get_log_in_out_links_and_user())
        
        self.render_response("create.html", **context)

    def post(self):
        context = {}

        post_body = self.request.POST

        po_id = None
        try:
            is_multiline = post_body.get("multiline-po")
            purchaser = post_body["email"]
            supplier = post_body["supplier"]
            if not is_multiline:
                product = post_body["product"]
            else:
                product = post_body["multiline-product"]
                product = product.replace("\r\n", "<br />")
                product = product.replace("\n", "<br />")
            price = post_body["price"]
            # Strip any $ or , from the price
            price = price.replace("$", "").replace(",", "")
            account_code = post_body.get("accountcode")

            po_id = create_purchase_order(purchaser, supplier, product, price, account_code=account_code)
        except (ValueError, KeyError) as ve:
            context["form"] = {
                "purchaser": purchaser,
                "supplier": supplier,
                "product": product,
                "price": price,
                "account_code": account_code
            }
            context["errors"] = [ve.message]

        if po_id:
            context["success"] = True
            context["po_id"] = po_id
            send_admin_email_for_new_po(po_id)

        self.get(**context)


