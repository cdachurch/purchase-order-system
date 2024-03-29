"""
Model code
"""
from google.cloud import ndb


class BaseModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.DateTimeProperty()
