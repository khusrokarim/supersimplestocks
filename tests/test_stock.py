import unittest
from datetime import datetime, timedelta
from decimal import Decimal

from super_simple_stocks import Stock, Exchange, Trade, InvalidOperation


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

    def test_dividend_yield(self):
        exchange = Exchange('Test Exchange')
        stock = Stock('TEST', 'common', 100, 10)
        exchange.add_stock(stock)
        stock.record_trade(10, 'buy', 2)
        stock.record_trade(20, 'sell', 2)
        stock.record_trade(30, 'buy', 3)
        self.assertEqual(stock.dividend_yield(), 4)
        stock = Stock('TESTPREFERRED', 'preferred', 100, 10, Decimal('0.25'))
        exchange.add_stock(stock)
        stock.record_trade(10, 'buy', 2)
        stock.record_trade(20, 'sell', 2)
        stock.record_trade(30, 'buy', 3)
        self.assertEqual(stock.dividend_yield(), 10)

    def test_pe_ratio(self):
        exchange = Exchange('Test Exchange')
        stock = Stock('TEST', 'common', 100, 10)
        exchange.add_stock(stock)
        stock.record_trade(10, 'buy', 2)
        stock.record_trade(20, 'sell', 2)
        stock.record_trade(30, 'buy', 3)
        self.assertEqual(stock.pe_ratio(), Decimal('0.25'))

    def test_price(self):
        exchange = Exchange('Test Exchange')
        stock = Stock('TEST', 'common', 100)
        exchange.add_stock(stock)
        self.assertIsNone(stock.price())
        stock.record_trade(10, 'buy', 2)
        stock.record_trade(20, 'sell', 2)
        stock.record_trade(30, 'buy', 3)
        self.assertEqual(stock.price(), Decimal('2.5'))
        new_trades = []
        for trade in exchange.trades[stock.symbol]:
            six_minutes_ago = datetime.utcnow() - timedelta(minutes=6)
            new_trades.append(
                Trade(
                    date_time=six_minutes_ago,
                    symbol=trade.symbol,
                    quantity=trade.quantity,
                    buy_or_sell=trade.buy_or_sell,
                    price=trade.price,
                )
            )
        exchange.trades[stock.symbol] = new_trades
        self.assertEqual(stock.price(), 3)



class TestExchange(unittest.TestCase):

    def setUp(self):
        self.exchange = Exchange('Test Exchange')

    def test_create_exchange(self):
        self.assertEqual(self.exchange.name, 'Test Exchange')

    def test_add_stock(self):
        stock = Stock('TEST', 'common', 100)
        self.exchange.add_stock(stock)
        self.assertEqual(self.exchange.stocks[stock.symbol], stock)

    def test_record_trade(self):
        stock = Stock('TEST', 'common', 100)
        with self.assertRaises(AttributeError):
            stock.record_trade(10, 'buy', 300)
        self.exchange.add_stock(stock)
        stock.record_trade(10, 'buy', 300)
        trade = self.exchange.trades[stock.symbol][0]
        self.assertEqual(trade.symbol, stock.symbol)
        self.assertEqual(trade.quantity, 10)
        self.assertEqual(trade.price, 300)
        with self.assertRaises(ValueError):
            stock.record_trade(-4, 'buy', 300)
        with self.assertRaises(ValueError):
            stock.record_trade(10, 'discard', 300)
        with self.assertRaises(ValueError):
            stock.record_trade(10, 'buy', -1)
