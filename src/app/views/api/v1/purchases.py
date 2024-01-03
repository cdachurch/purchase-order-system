"""
Purchases api endpoints
"""
from flask import Blueprint
from google.cloud import ndb

from app.utility.mailer import send_message
from app.views.api.v1 import API_CONSTANTS
from app.domain.purchase import (
    approve_purchase_order,
    cancel_purchase_order,
    create_interim_purchase_order,
    deny_purchase_order,
    get_purchase_order_entity,
)
from app.domain.user import check_and_return_user

client = ndb.Client()

bp = Blueprint("purchase_api", __name__, url_prefix="/api/v1/purchase")


@bp.post("/create/interim/")
def create_interim_po():
    po_entity = None
    po_entity = create_interim_purchase_order()
    return {"data": {"po_id": po_entity.po_id, "pretty_po_id": po_entity.pretty_po_id}}


@bp.get("/accept/<po_id>/")
def accept_po(po_id):
    if not po_id:
        return {"data": "Error"}, 400

    with client.context():
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            approver, _, _ = check_and_return_user()
            approve_purchase_order(po_entity, approver["name"])
            send_email(po_entity.purchaser, API_CONSTANTS.ACCEPTED, po_entity)
            return {"data": {}}


@bp.get("/cancel/<po_id>/")
def cancel_po(po_id):
    if not po_id:
        return {"data": "Error"}, 400

    with client.context():
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            cancel_purchase_order(po_entity)
            return {"data": {}}


@bp.get("/deny/<po_id>/")
def deny_po(po_id):
    if not po_id:
        return {"data": "Error"}, 400

    with client.context():
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            deny_purchase_order(po_entity)
            send_email(po_entity.purchaser, API_CONSTANTS.DENIED, po_entity)
            return {"status": 200}


@bp.get("/invoice/<po_id>/")
def invoice_po(po_id):
    if not po_id:
        return {"data": "Error"}, 400

    with client.context():
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            # flip that bit
            po_entity.is_invoiced = not po_entity.is_invoiced
            po_entity.put()
            return {"status": 200}


def send_email(to, how, po_entity):
    supplier = po_entity.supplier
    product = po_entity.product
    price = po_entity.price
    pretty_po_id = po_entity.pretty_po_id
    if all([supplier, product, price, pretty_po_id]):
        if how == API_CONSTANTS.ACCEPTED:
            send_message(
                to,
                API_CONSTANTS.ACCEPTED_SUBJECT,
                html=API_CONSTANTS.ACCEPTED_EMAIL_HTML.format(
                    price,
                    ppoid=str(pretty_po_id).zfill(4),
                    supplier=supplier,
                    product=product,
                ),
            )
        elif how == API_CONSTANTS.DENIED:
            send_message(
                to,
                API_CONSTANTS.DENIED_SUBJECT,
                html=API_CONSTANTS.DENIED_EMAIL_HTML.format(
                    price,
                    ppoid=str(pretty_po_id).zfill(4),
                    supplier=supplier,
                    product=product,
                ),
            )
