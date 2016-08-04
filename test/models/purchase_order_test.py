"""
PurchaseOrder model tests.
"""
from google.appengine.ext import ndb

from app.domain.user import create_user
from app.models.purchaseorder import PurchaseOrder
from test.fixtures.appengine import GaeTestCase

class PurchaseOrderModelTests(GaeTestCase):
    def setUp(self):
        super(PurchaseOrderModelTests, self).setUp()
        self.name = "Testing"
        self.email = "testing@rocks.com"
        self.user_id = "123456789"
        self.user1 = create_user(self.name, self.email, self.user_id)

        self.name2 = "Testing2"
        self.email2 = "testing@muchrocks.com"
        self.user_id2 = "987654321"
        self.user2 = create_user(self.name2, self.email2, self.user_id2)

    def createPurchaseOrders(self, getEntities=False):
        self.po_keys = [
            PurchaseOrder(po_id='1234',
                pretty_po_id=1,
                key=PurchaseOrder.build_key('1234'),
                product='Test Widgets',
                supplier='Test Widget Co.',
                purchaser=self.email,
                price=19.99).put(),
            PurchaseOrder(po_id='1235',
                pretty_po_id=2,
                key=PurchaseOrder.build_key('1235'),
                product='Test Widgets 2',
                supplier='Test Widget Co. 2',
                purchaser=self.email2,
                price=29.99).put(),
            PurchaseOrder(po_id='1236',
                pretty_po_id=3,
                key=PurchaseOrder.build_key('1236'),
                product='Test Widgets 3',
                supplier='Test Widget Co. 3',
                purchaser=self.email2,
                price=39.99).put(),
            PurchaseOrder(po_id='1237',
                pretty_po_id=4,
                key=PurchaseOrder.build_key('1237'),
                product='Test Widgets 4',
                supplier='Test Widget Co. 4',
                purchaser=self.email,
                price=49.99).put(),
            PurchaseOrder(po_id='1238',
                pretty_po_id=5,
                key=PurchaseOrder.build_key('1238'),
                product='Test Widgets 5',
                supplier='Test Widget Co. 5',
                purchaser=self.email,
                price=59.99).put(),
            ]

        if getEntities:
            # If they want them, load all of the entities themselves into the class.
            self.po_entities = map(lambda x: x.get(), self.po_keys)

    def tearDown(self):
        super(PurchaseOrderModelTests, self).tearDown()

    def test_build_key_returns_key(self):
        key = PurchaseOrder.build_key('1234')
        self.assertIsInstance(key, ndb.Key)
        self.assertEqual('1234', key.id())

    def test_get_next_ppoid_returns_1_when_no_other_pos_exist(self):
        next_ppoid = PurchaseOrder.get_next_pretty_po_id()
        self.assertEqual(1, next_ppoid)

    def test_get_next_ppoid_returns_next_id_when_pos_exist(self):
        self.createPurchaseOrders()
        next_ppoid = PurchaseOrder.get_next_pretty_po_id()
        self.assertEqual(6, next_ppoid)

    def test_get_all_purchase_orders_limit_must_be_integer(self):
        with self.assertRaises(ValueError):
            PurchaseOrder.get_all_purchase_orders('not an integer')

    def test_get_all_purchase_orders_retrieves_purchase_orders(self):
        self.createPurchaseOrders(True)
        pos = PurchaseOrder.get_all_purchase_orders()
        self.assertEqual(self.po_entities, pos)

    def test_get_all_purchase_orders_retrieves_first_X_purchase_orders_in_order(self):
        self.createPurchaseOrders(True)
        pos = PurchaseOrder.get_all_purchase_orders(2)
        self.assertEqual(self.po_entities[0:2], pos)

        loop = 0
        for po in pos:
            self.assertEqual(self.po_entities[loop].pretty_po_id, po.pretty_po_id)
            loop = loop + 1

    def test_get_all_purchase_orders_and_order_by_pretty_po_id_must_have_order_direction(self):
        with self.assertRaises(ValueError):
            PurchaseOrder.get_all_purchase_orders_and_order_by_pretty_po_id(None)

    def test_get_all_purchase_orders_and_order_by_pretty_po_id_retrieves_pos_in_order(self):
        self.createPurchaseOrders()
        pos = PurchaseOrder.get_all_purchase_orders_and_order_by_pretty_po_id('ASC')
        self.assertEqual(1, pos[0].pretty_po_id)
        self.assertEqual(2, pos[1].pretty_po_id)

    def test_get_all_purchase_orders_and_order_by_pretty_po_id_limit_must_be_integer(self):
        with self.assertRaises(ValueError):
            PurchaseOrder.get_all_purchase_orders_and_order_by_pretty_po_id('ASC', 'one')

    def test_get_purchase_orders_by_purchaser_must_provide_purchaser(self):
        with self.assertRaises(ValueError):
            PurchaseOrder.get_purchase_orders_by_purchaser(None)

    def test_get_purchase_orders_by_purchaser_returns_correct_results(self):
        self.createPurchaseOrders()
        pos = PurchaseOrder.get_purchase_orders_by_purchaser(self.email)
        self.assertEqual(pos[0].purchaser, self.email)

    def test_to_dict_returns_dictionary(self):
        self.createPurchaseOrders()
        po = self.po_keys[0].get()
        po_dict = po.to_dict()
        self.assertIsInstance(po_dict, dict)
        self.assertEqual(po_dict['purchaser'], po.purchaser)
