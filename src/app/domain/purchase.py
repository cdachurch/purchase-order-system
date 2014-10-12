"""
Domain code for purchase orders
"""
import uuid

from app.domain.user import check_and_return_user
from app.models.purchaseorder import PurchaseOrder
from app.utility.mailer import send_message
from settings import APPROVAL_ADMINS, SERVER_ADDRESS


def create_purchase_order(purchaser, supplier, product, price, po_id=None):
    """ Creates a purchase order """
    if not purchaser:
        raise ValueError("purchaser is a required field")
    if not supplier:
        raise ValueError("supplier is a required field")
    if not product:
        raise ValueError("product is a required field")
    if not price:
        raise ValueError("price is a required field")
    if not po_id:
        # generate a unique string
        po_id = str(uuid.uuid4()).split("-")[-1]

    new_po = PurchaseOrder(key=PurchaseOrder.build_key(po_id))

    new_po.po_id = po_id
    new_po.pretty_po_id = PurchaseOrder.get_next_pretty_po_id()
    new_po.purchaser = purchaser
    new_po.supplier = supplier
    new_po.product = product
    new_po.price = float(price)

    new_po.put()

    return po_id


def get_purchase_order_entity(po_id):
    """
    Get a purchase order entity by id
    """
    po_key = PurchaseOrder.build_key(po_id);
    po = po_key.get()
    if po:
        return po


def get_purchase_order_to_dict(po_id=None, pretty_po_id=None):
    """ 
    Takes either a po_id or pretty_po_id to return that purchase order's dictionary representation
    """
    if po_id:
        purchase_order = PurchaseOrder.build_key(po_id).get()
        if purchase_order:
            return purchase_order.to_dict()
        else:
            raise ValueError("Couldn't find a purchase order with po_id of %s" % po_id)


def get_all_purchase_orders(limit=None):
    return PurchaseOrder.get_all_purchase_orders(limit=limit)


def send_admin_email_for_new_po(po_id):
    po_dict = get_purchase_order_to_dict(po_id=po_id)
    if not po_dict:
        raise ValueError("There is no purchase order for this po_id: %s" % po_id)

    _, user, _, _ = check_and_return_user() 
    username = user.email
    real_name = user.name;
    supplier = po_dict["supplier"]
    product = po_dict["product"]
    price = po_dict["price"]
    approval_link = "%spurchase/%s/" % (SERVER_ADDRESS, po_id)

    subject = "%s has made a purchase order request" % real_name

    email_template = """
        <p>Hello,</p>
        <p>A person with email {username} has made a purchase order request for the following:</p>
        <ul>
            <li>Supplier: {supplier}</li>
            <li>Product: {product}</li>
            <li>Price: ${price}</li>
        </ul>
        <p>To approve or deny this request, click <a href='{approval_link}'>here</a>.</p>
        <p>Thank you, and have a great day!</p>
    """.format(username=username, supplier=supplier, product=product, price=price, 
               approval_link=approval_link)

    send_message(APPROVAL_ADMINS, subject, html=email_template)
