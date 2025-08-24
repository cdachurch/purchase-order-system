"""
Domain code for purchase orders

These functions should be called from within an ndb client context, they won't create their own
"""

import logging
import uuid

from html_sanitizer import Sanitizer

from app.basecamp.todos import create_todo_item, update_todo_item
from app.domain.user import get_current_ndb_user, get_current_user
from app.models.purchaseorder import PurchaseOrder
from app.basecamp.chatbot import send_message
from settings import (
    ENVIRONMENT,
    SERVER_ADDRESS,
)


def approve_purchase_order(po_entity, approver):
    """Mark a purchase order as approved"""
    if not isinstance(po_entity, PurchaseOrder):
        raise ValueError("The purchase order entity must be passed to this function")
    if not approver:
        raise ValueError("A purchase order must be approved by someone")
    po_entity.approved_by = approver
    po_entity.is_approved = True
    logging.info(
        "%s approved po# %s (%s)",
        approver,
        po_entity.po_id,
        po_entity.pretty_po_id,
    )

    po_entity.put()

    user = get_current_ndb_user()

    perma_link = "%spurchase/%s/" % (SERVER_ADDRESS, po_entity.po_id)
    update_todo_item(
        po_entity.todo_url,
        user.basecamp_access_token,
        f"#{po_entity.pretty_po_id} for {po_entity.purchaser} ✅",
        f"<p><a href='{perma_link}'>This PO</a> is approved ✅ - make sure to get your invoice to Des once you have one.</p>",
        user.basecamp_assignee_id,
    )
    send_message(
        '<p>Purchase order <a href="{approval_link}">#{ppo_id}</a> approved ✅</p>'.format(
            approval_link=perma_link,
            ppo_id=str(po_entity.pretty_po_id).zfill(4),
        )
    )


def cancel_purchase_order(po_entity):
    """Mark a purchase order as cancelled, clearing the approved or denied status as well"""
    if not isinstance(po_entity, PurchaseOrder):
        raise ValueError("The purchase order entity must be passed to this function")

    is_being_canceled = po_entity.is_cancelled == False
    po_entity.is_cancelled = not po_entity.is_cancelled
    po_entity.is_approved = False
    po_entity.is_denied = False
    logging.info("po# %s (%s) was cancelled", po_entity.po_id, po_entity.pretty_po_id)
    po_entity.put()

    icon = "🚫" if is_being_canceled else "💌"
    prefix = "" if is_being_canceled else "un"
    perma_link = "%spurchase/%s/" % (SERVER_ADDRESS, po_entity.po_id)
    user = get_current_ndb_user()
    update_todo_item(
        po_entity.todo_url,
        user.basecamp_access_token,
        f"#{po_entity.pretty_po_id} for {po_entity.purchaser} {icon}",
        f"<p><a href='{perma_link}'>This PO</a> has been {prefix}cancelled {icon}</p>",
        user.basecamp_assignee_id,
    )
    send_message(
        '<p>Purchase order <a href="{perma_link}">#{ppo_id}</a> {prefix}cancelled {icon}</p>'.format(
            perma_link=perma_link,
            ppo_id=str(po_entity.pretty_po_id).zfill(4),
            icon=icon,
            prefix=prefix,
        )
    )


def create_purchase_order(
    purchaser, supplier, product, price, po_id=None, account_code=None
):
    """Creates a purchase order"""
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
        logging.info(f"fetched po by supplied id {po_id}")
    else:
        new_po = PurchaseOrder(key=PurchaseOrder.build_key(generated_po_id))
        new_po.po_id = generated_po_id
        new_po.pretty_po_id = PurchaseOrder.get_next_pretty_po_id()
        po_id = generated_po_id
        logging.info(f"created new po object with id: {po_id}, {new_po.pretty_po_id}")

    split_purchaser = purchaser.split("@")
    # Always take what's before the @, never "whoever@cdac.ca"
    new_po.purchaser = split_purchaser[0]
    new_po.supplier = supplier
    sanitizer = Sanitizer()
    new_po.product = sanitizer.sanitize(product)
    if account_code:
        new_po.account_code = account_code
    new_po.price = float(price)

    logging.info(new_po)
    logging.info(f"creating new po {new_po.po_id}, {new_po.pretty_po_id}")

    perma_link = "%spurchase/%s/" % (SERVER_ADDRESS, new_po.po_id)
    user = get_current_ndb_user()
    todo_url = create_todo_item(
        user.basecamp_todos_url,
        user.basecamp_access_token,
        f"#{new_po.pretty_po_id} for {new_po.purchaser}",
        f"<p>To approve or deny this request, click <a href='{perma_link}'>here</a>.</p>",
    )
    new_po.todo_url = todo_url
    new_po.put()

    message_template = """
        <p>Purchase order <a href='{perma_link}'>#{ppo_id}</a> created 🆕</p>
    """.format(
        perma_link=perma_link,
        ppo_id=str(new_po.pretty_po_id).zfill(4),
    )

    send_message(message_template)

    return new_po.po_id


def create_interim_purchase_order():
    """Creates an interim purchase order, to be finalized later"""
    po_id = str(uuid.uuid4()).split("-")[-1]

    new_po = PurchaseOrder(key=PurchaseOrder.build_key(po_id))
    new_po.po_id = po_id
    new_po.pretty_po_id = PurchaseOrder.get_next_pretty_po_id()
    new_po.put()

    # Get current user because we haven't added the purchaser yet
    user = get_current_user()
    logging.info(f"interim po created by {user["name"]}: {new_po}")
    return new_po


def deny_purchase_order(po_entity):
    """Mark a purchase order as denied"""
    if not isinstance(po_entity, PurchaseOrder):
        raise ValueError("The purchase order entity must be passed to this function")

    po_entity.is_denied = True
    logging.info("po# %s (%s) was just denied", po_entity.po_id, po_entity.pretty_po_id)
    po_entity.put()
    user = get_current_ndb_user()
    perma_link = "%spurchase/%s/" % (SERVER_ADDRESS, po_entity.po_id)
    update_todo_item(
        po_entity.todo_url,
        user.basecamp_access_token,
        f"#{po_entity.pretty_po_id} for {po_entity.purchaser} ❌",
        f"<p><a href='{perma_link}'>This PO</a> has been denied ❌</p>",
        user.basecamp_assignee_id,
    )
    send_message(
        '<p>Purchase order <a href="{perma_link}">#{ppo_id}</a> denied ❌</p>'.format(
            perma_link=perma_link,
            ppo_id=str(po_entity.pretty_po_id).zfill(4),
        )
    )


def get_purchase_order_entity(po_id):
    """Get a purchase order entity by id"""
    po_key = PurchaseOrder.build_key(po_id)
    return po_key.get()


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
        return po_entity.to_dict()
