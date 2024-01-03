"""
Views for purchase orders
"""
from flask import Blueprint, redirect, url_for, request, session
from google.cloud import ndb

from app.domain.purchase import (
    create_purchase_order,
    get_purchase_order_to_dict,
    send_admin_email_for_new_po,
)
from app.views import render_po_template
from app.workflow.user import get_log_in_out_links_and_user

bp = Blueprint("purchase", __name__, url_prefix="/purchase")

client = ndb.Client()


@bp.route("/")
def top_500():
    if "email" not in session:
        return redirect("/")

    bread_crumbs = [("Home", url_for("index")), ("List purchase orders", None)]

    context = {
        # "purchase_orders": get_all_purchase_orders(),
        "bread_crumbs": bread_crumbs
    }

    # Add the login/out links and the user info
    context.update(get_log_in_out_links_and_user())

    return render_po_template("purchaseorders.html", **context)


@bp.route("/<po_id>/")
def purchase_view(po_id):
    bread_crumbs = [
        ("Home", url_for("index")),
        ("List purchase orders", url_for("purchase.top_500")),
        ("View purchase order", None),
    ]

    context = {}

    # Add the login/out links and the user info
    context.update(get_log_in_out_links_and_user())

    with client.context():
        try:
            po_dict = get_purchase_order_to_dict(po_id=po_id)
        except ValueError:
            return render_po_template("404.html", **context)

        context.update(po_dict)
    context["bread_crumbs"] = bread_crumbs

    return render_po_template("purchase.html", **context)


@bp.route("/all/")
def all_purchases():
    bread_crumbs = [("Home", url_for("index")), ("List purchase orders", None)]

    context = {
        # "purchase_orders": get_all_purchase_orders(),
        "bread_crumbs": bread_crumbs
    }

    # Add the login/out links and the user info
    context.update(get_log_in_out_links_and_user())

    return render_po_template("purchaseorders.html", **context)


@bp.get("/create/")
def create_purchase(**context):
    bread_crumbs = [
        ("Home", url_for("index")),
        ("List purchase orders", url_for("purchase.top_500")),
        ("Create purchase order", None),
    ]
    if not context:
        context = {}
    context["bread_crumbs"] = bread_crumbs
    if not context.get("form", None):
        context["form"] = {}

    return render_po_template("create.html", **context)


@bp.post("/create/")
def create_purchase_post():
    context = {}

    # https://flask.palletsprojects.com/en/3.0.x/quickstart/#the-request-object
    post_body = request.form

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
        _po_id = post_body.get("_poid")
        # Strip any $ or , from the price
        price = price.replace("$", "").replace(",", "")
        account_code = post_body.get("accountcode")

        po_id = create_purchase_order(
            purchaser,
            supplier,
            product,
            price,
            po_id=_po_id,
            account_code=account_code,
        )
    except (ValueError, KeyError) as ve:
        context["form"] = {
            "purchaser": purchaser,
            "supplier": supplier,
            "product": product,
            "price": price,
            "account_code": account_code,
        }
        context["errors"] = [str(ve)]

    if po_id:
        context["success"] = True
        context["po_id"] = po_id
        send_admin_email_for_new_po(po_id)

    return create_purchase(**context)
