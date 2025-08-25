"""
Purchases api endpoints
"""

from flask import Blueprint
from google.cloud import ndb

from app.domain.purchase import (
    approve_purchase_order,
    cancel_purchase_order,
    create_interim_purchase_order,
    deny_purchase_order,
    get_purchase_order_entity,
    invoice_purchase_order,
)
from app.domain.user import check_and_return_user

client = ndb.Client()

bp = Blueprint("purchase_api", __name__, url_prefix="/api/v1/purchase")


@bp.post("/create/interim/")
def create_interim_po():
    po_entity = None
    with client.context():
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
            return {"status": 200}


@bp.get("/invoice/<po_id>/")
def invoice_po(po_id):
    if not po_id:
        return {"data": "Error"}, 400

    with client.context():
        po_entity = get_purchase_order_entity(po_id)
        if po_entity:
            invoice_purchase_order(po_entity)
            return {"status": 200}
