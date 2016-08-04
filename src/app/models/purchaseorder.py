"""
Purchase order model
"""
from google.appengine.ext import ndb

from app.models import BaseModel

class PurchaseOrder(BaseModel):
    """
    PurchaseOrder model
    """
    po_id = ndb.StringProperty()
    pretty_po_id = ndb.IntegerProperty(indexed=True)
    purchaser = ndb.StringProperty()
    supplier = ndb.StringProperty()
    product = ndb.StringProperty()
    price = ndb.FloatProperty()
    approved_by = ndb.StringProperty()
    account_code = ndb.StringProperty()
    # these default to False (perfect!)
    is_approved = ndb.BooleanProperty()
    is_denied = ndb.BooleanProperty()
    is_invoiced = ndb.BooleanProperty()
    is_cancelled = ndb.BooleanProperty()

    is_addressed = ndb.ComputedProperty(lambda self: self.is_approved or self.is_denied or self.is_cancelled)

    VALID_ORDER_DIRECTIONS = ["ASC", "DESC"]

    @classmethod
    def build_key(cls, po_id):
        """ Build and return a PurchaseOrder key """
        key = ndb.Key(cls, po_id)
        return key

    def to_dict(self):
        return {
            "po_id": self.po_id,
            "pretty_po_id": self.pretty_po_id,
            "purchaser": self.purchaser,
            "supplier": self.supplier,
            "product": self.product,
            "price": self.price,
            "account_code": self.account_code,
            "is_approved": self.is_approved,
            "is_denied": self.is_denied,
            "is_addressed": self.is_addressed,
            "is_invoiced": self.is_invoiced,
            "is_cancelled": self.is_cancelled,
            "approved_by": self.approved_by,
            "created_date": self.created.strftime('%Y-%m-%d') if self.created else None,
            "last_updated": self.updated.strftime('%Y-%m-%d') if self.updated else None,
            "deleted_date": self.deleted.strftime('%Y-%m-%d') if self.deleted else None,
        }

    @classmethod
    def get_next_pretty_po_id(cls):
        query = cls.query().order(-cls.pretty_po_id)

        if query.count():
            current_highest_ppoid = query.iter().next().pretty_po_id
            # If it exists, increment it by one to get the next number,
            # otherwise just return 1 as there may not be any POs yet.
            return current_highest_ppoid + 1 if current_highest_ppoid else 1
        else:
            return 1


    @classmethod
    def get_all_purchase_orders(cls, limit=None):
        """ Gets all purchase orders, ordered by pretty po id """
        if limit and not isinstance(limit, int):
            raise ValueError("limit must be an integer")
        query = cls.query().order(cls.pretty_po_id)
        return query.fetch(limit=limit)

    @classmethod
    def get_all_purchase_orders_and_order_by_pretty_po_id(cls, order_direction, limit=None):
        """ Get all purchase orders, ordered by pretty_po_id """
        if not order_direction:
            raise ValueError("order direction must be provided (ASC, DESC)")
        if limit and not isinstance(limit, int):
            raise ValueError("limit must be an integer")
        query = cls.query().order(cls.pretty_po_id) if order_direction == "ASC" else \
                    cls.query().order(-cls.created)
        return query.fetch(limit=limit)

    @classmethod
    def get_purchase_orders_by_purchaser(cls, purchaser, limit=None):
        """ Get purchase orders with a query """
        if not purchaser:
            raise ValueError("purchaser (email address) must be provided")
        query = cls.gql("WHERE purchaser = :1", purchaser)
        return query.fetch(limit=limit)
