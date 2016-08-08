""" Tests for domain/purchase """
import unittest

import mock

from app.domain.purchase import get_purchase_orders_by_purchaser


class GetPurchaseOrdersByPurchaserTests(unittest.TestCase):
    @mock.patch('app.domain.purchase.memcache.get', new=mock.MagicMock(return_value=['test po']))
    def test_uses_memcached_results_if_they_exist(self):
        pos = get_purchase_orders_by_purchaser('some_guy')
        self.assertEqual(['test po'], pos)

    @mock.patch('app.domain.purchase.memcache', new=mock.MagicMock(get=mock.MagicMock(return_value=None)))
    @mock.patch('app.domain.purchase.PurchaseOrder.get_purchase_orders_by_purchaser', return_value=['stuff'])
    def test_gets_fresh_results_if_no_memcache_results_available(self, get_po_mock):
        get_purchase_orders_by_purchaser('some_guy')
        get_po_mock.assert_called_once_with('some_guy', limit=mock.ANY)
