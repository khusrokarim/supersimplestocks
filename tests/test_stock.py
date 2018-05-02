import unittest
from decimal import Decimal

from super_simple_stocks import Stock, Exchange


class TestStock(unittest.TestCase):

    def test_create_stock(self):
        stock = Stock('TEST', 'common', 100)
        self.assertIsInstance(stock, Stock)
        stock = Stock('TEST', 'preferred', 100, last_dividend=1, fixed_dividend=Decimal('0.02'))
        self.assertIsInstance(stock, Stock)
        with self.assertRaises(ValueError):
            Stock('TEST', 'invalid type', 100)
        with self.assertRaises(ValueError):
            Stock('TEST', 'common', -5)

    # def test_dividend_yield(self):
    #     self.fail()

    # def test_pe_ratio(self):
    #     self.fail()

    # def test_record_trade(self):
    #     self.fail()

    # def test_price(self):
    #     self.fail()

class TestExchange(unittest.TestCase):

    def test_create_exchange(self):
        exchange = Exchange('Test Exchange')
        self.assertEqual(exchange.name, 'Test Exchange')
