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
    # these default to False (perfect!)
    is_approved = ndb.BooleanProperty()
    is_denied = ndb.BooleanProperty()
    is_addressed = ndb.ComputedProperty(lambda self: self.is_approved or self.is_denied)

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
            "is_approved": self.is_approved,
            "is_denied": self.is_denied,
            "is_addressed": self.is_addressed,
            "created_date": self.created,
            "last_updated": self.updated,
            "deleted_date": self.deleted,
        }

    @classmethod
    def get_next_pretty_po_id(cls):
        counter = 1
        found_unique = False
        while not found_unique:
            query = cls.query(cls.pretty_po_id == counter)
            # Check if the pretty po id is attached to a po already
            if not query.iter().has_next():
                found_unique = True
            else:
                counter += 1
        return counter

    @classmethod
    def get_all_purchase_orders(cls, limit=None):
        """ Gets all purchase orders, ordered by pretty po id """
        if limit and not isinstance(limit, int):
            raise ValueError("limit must be an integer")
        query = cls.query().order(cls.pretty_po_id)
        return query.fetch(limit=limit)
