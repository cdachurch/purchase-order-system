"""
Domain code for purchase orders
"""
import logging
import uuid

from app.domain.user import check_and_return_user
from app.models.purchaseorder import PurchaseOrder
from app.utility.mailer import send_message
from settings import APPROVAL_ADMINS, ENVIRONMENT, SERVER_ADDRESS


def approve_purchase_order(po_entity, approver):
    """ Mark a purchase order as approved """
    if not isinstance(po_entity, PurchaseOrder):
        raise ValueError("The purchase order entity must be passed to this function")
    if not approver:
        raise ValueError("A purchase order must be approved by someone")
    po_entity.approved_by = approver.name
    po_entity.is_approved = True
    logging.info("%s approved po# %s (%s)", approver.name, po_entity.po_id, po_entity.pretty_po_id)
    po_entity.put()
    return po_entity


def cancel_purchase_order(po_entity):
    """ Mark a purchase order as cancelled, clearing the approved or denied status as well """
    if not isinstance(po_entity, PurchaseOrder):
        raise ValueError("The purchase order entity must be passed to this function")

    po_entity.is_cancelled = not po_entity.is_cancelled
    po_entity.is_approved = False
    po_entity.is_denied = False
    logging.info("po# %s (%s) was cancelled", po_entity.po_id, po_entity.pretty_po_id)
    po_entity.put()


def create_purchase_order(purchaser, supplier, product, price, po_id=None, account_code=None):
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
        generated_po_id = str(uuid.uuid4()).split("-")[-1]

    if po_id:
        new_po_key = PurchaseOrder.build_key(po_id)
        new_po = new_po_key.get()
        logging.info(new_po)
    else:
        new_po = PurchaseOrder(key=PurchaseOrder.build_key(generated_po_id))
        new_po.po_id = generated_po_id
        new_po.pretty_po_id = PurchaseOrder.get_next_pretty_po_id()
        po_id = generated_po_id

    new_po.purchaser = purchaser if purchaser.find("@") else purchaser + "@cdac.ca"
    new_po.supplier = supplier
    new_po.product = product
    if account_code:
        new_po.account_code = account_code
    new_po.price = float(price)

    new_po.put()

    return po_id


def create_interim_purchase_order():
    """ Creates an interim purchase order, to be finalized later """
    po_id = str(uuid.uuid4()).split("-")[-1]
    new_po = PurchaseOrder(key=PurchaseOrder.build_key(po_id))

    new_po.po_id = po_id
    new_po.pretty_po_id = PurchaseOrder.get_next_pretty_po_id()
    new_po.put()

    return new_po


def deny_purchase_order(po_entity):
    """ Mark a purchase order as denied """
    if not isinstance(po_entity, PurchaseOrder):
        raise ValueError("The purchase order entity must be passed to this function")
    po_entity.is_denied = True
    logging.info("po# %s (%s) was just denied", po_entity.po_id, po_entity.pretty_po_id)
    po_entity.put()


def get_purchase_order_entity(po_id):
    """ Get a purchase order entity by id """
    po_key = PurchaseOrder.build_key(po_id);
    po = po_key.get()
    if po:
        return po


def get_purchase_order_to_dict(po_id=None, pretty_po_id=None, po_entity=None):
    """
    Takes either a po_id or pretty_po_id to return that purchase order's dictionary representation
    """
    if po_id:
        purchase_order = PurchaseOrder.build_key(po_id).get()
        if purchase_order:
            return purchase_order.to_dict()
        else:
            raise ValueError("Couldn't find a purchase order with po_id of %s" % po_id)
    elif po_entity:
        return po_entity.to_dict() if isinstance(po_entity, PurchaseOrder) else None


def get_all_purchase_orders(order_direction=None, limit=None):
    purchase_orders = None
    if order_direction in PurchaseOrder.VALID_ORDER_DIRECTIONS:
        purchase_orders = PurchaseOrder.get_all_purchase_orders_and_order_by_pretty_po_id(order_direction,
                                                                                          limit=limit)
    else:
        purchase_orders = PurchaseOrder.get_all_purchase_orders(limit=limit)

    return purchase_orders


def get_purchase_orders_by_purchaser(purchaser, limit=None):
    return PurchaseOrder.get_purchase_orders_by_purchaser(purchaser, limit=limit)


def send_admin_email_for_new_po(po_id):
    po_dict = get_purchase_order_to_dict(po_id=po_id)
    if not po_dict:
        raise ValueError("There is no purchase order for this po_id: %s" % po_id)

    _, user, _, _, _ = check_and_return_user()
    username = user.email if user.email.find("@") else user.email + "@cdac.ca"
    real_name = user.name;
    supplier = po_dict["supplier"]
    product = po_dict["product"]
    price = po_dict["price"]
    approval_link = "%spurchase/%s/" % (SERVER_ADDRESS, po_id)

    subject = "%s has made a purchase order request" % real_name

    if ENVIRONMENT == "DEMO":
        subject += " on %s" % ENVIRONMENT

    email_template = """
        <p>Hello,</p>
        <p>{real_name} has made a purchase order request for the following:</p>
        <ul>
            <li>Supplier: {supplier}</li>
            <li>Product: {product}</li>
            <li>Price: ${:,.2f}</li>
        </ul>
        <p>To approve or deny this request, click <a href='{approval_link}'>here</a>.</p>
        <p>Thank you, and have a great day!</p>
    """.format(price, real_name=real_name, supplier=supplier, product=product,
               approval_link=approval_link)

    send_message(APPROVAL_ADMINS, subject, html=email_template)
