"""
Views for purchase orders
"""
import logging

from app.domain.purchase import create_purchase_order, get_purchase_order_to_dict, \
                                get_all_purchase_orders, send_admin_email_for_new_po
from app.views import TemplatedView
from app.workflow.user import get_log_in_out_links_and_user

class PurchaseView(TemplatedView):
    def get(self, po_id):
        bread_crumbs = [
            ("Home", self.uri_for('index')),
            ("List purchase orders", self.uri_for("list_purchases")),
            ("View purchase order", None)
        ]
        po_dict = get_purchase_order_to_dict(po_id=po_id)
        
        context = po_dict
        context["bread_crumbs"] = bread_crumbs

        # Add the login/out links and the user info
        context.update(get_log_in_out_links_and_user())

        self.render_response("purchase.html", **context)


class PurchaseListView(TemplatedView):
    def get(self):
        bread_crumbs = [
            ("Home", self.uri_for('index')),
            ("List purchase orders", None)
        ]
        context = {
            "purchase_orders": get_all_purchase_orders(),
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

        # Add the login/out links and the user info
        context.update(get_log_in_out_links_and_user())
        
        self.render_response("create.html", **context)

    def post(self):
        context = {}

        post_body = self.request.POST

        po_id = None
        try:
            purchaser = post_body["email"]
            supplier = post_body["supplier"]
            product = post_body["product"]
            price = post_body["price"]

            po_id = create_purchase_order(purchaser, supplier, product, price)
        except (ValueError, KeyError) as ve:
            context["errors"] = [ve.message]

        if po_id:
            context["success"] = True
            context["po_id"] = po_id
            send_admin_email_for_new_po(po_id)

        self.get(**context)


