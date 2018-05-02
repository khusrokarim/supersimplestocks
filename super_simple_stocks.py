from collections import defaultdict, namedtuple
from datetime import datetime, timedelta
from decimal import Decimal

from utils import validate_nonnegative, validate_member


Trade = namedtuple('Trade', ['date_time', 'symbol', 'quantity', 'buy_or_sell', 'price'])

class Stock:
    """A single stock, optionally traded on a single exchange."""

    stock_types = (
        'common',
        'preferred',
    )

    def __init__(self, symbol, stock_type, par_value, last_dividend=Decimal(), fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = validate_member('stock_type', stock_type, self.stock_types)
        self.par_value = validate_nonnegative('par_value', par_value)
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend

    def record_trade(self, quantity, buy_or_sell, price):
        """Record a trade of this stock"""
        self.exchange.record_trade(self.symbol, quantity, buy_or_sell, price)

    def price(self, minutes=5):
        """
        Calculate and return the volume weighted stock price over the last 5 minutes.
        If there were no trades in the last 5 minutes, return the price of the last trade.
        If the stock has not been traded, return None.
        """
        now = datetime.utcnow()
        calculate_since = now - timedelta(minutes=minutes)
        all_trades = self.exchange.trades[self.symbol]

        priced_trades = [
            trade for trade in all_trades
            if trade.date_time > calculate_since
        ]

        if not priced_trades:
            try:
                # No trades in the last 5 minutes
                priced_trades = [all_trades[-1]]
            except IndexError:
                # No trades at all
                return None

        numerator = sum((trade.price * trade.quantity for trade in priced_trades))
        denominator = sum((trade.quantity for trade in priced_trades))
        return numerator/denominator

    def dividend_yield(self):
        """
        Calculate and return the dividend yield of this stock.
        If a common stock has no last_dividend, return 0.
        Raises InvalidOperation if the stock has no price (because it has not been traded).
        """
        if not self.price():
            raise InvalidOperation('Dividend yield for {} cannot be calculated because it has no price')
        if self.stock_type == 'common':
            return (self.last_dividend or 0)/ self.price()
        else:
            return (self.fixed_dividend * self.par_value) / self.price()

    def pe_ratio(self):
        """Calculate P/E ratio"""
        # The given formula includes a variable 'dividend' without specifying fixed or last.
        # Since the examples do not include fixed dividends for common stock, and since
        # separate formulae are given for common and preferred where necessary (not for P/E ratio),
        # I will assume that the last dividend is relevant here.
        price = self.price()
        if (price is None) or not self.last_dividend:
            raise InvalidOperation((
                'P/E ratio cannot be calculated for {} '
                'because it has not distributed a dividend'
                ' or it does not have a price'
            ).format(self.symbol))
        return self.price() / self.last_dividend

    def __str__(self):
        return self.symbol

    @property
    def last_dividend(self):
        return self._last_dividend

    @last_dividend.setter
    def last_dividend(self, value):
        self._last_dividend = validate_nonnegative('last_dividend', value)

    @property
    def fixed_dividend(self):
        """Fixed dividend.  Required for preferred stocks."""
        return self._fixed_dividend

    @fixed_dividend.setter
    def fixed_dividend(self, value):
        if (self.stock_type == 'preferred') and (value is None):
            raise TypeError('Preferred stock must have a fixed dividend')
        self._fixed_dividend = validate_nonnegative('fixed_dividend', value, True)


class Exchange:
    """A stock exchange for trading individual Stocks."""

    def __init__(self, name):
        self.name = name
        self.stocks = {}
        self.trades = defaultdict(list)

    def add_stock(self, stock):
        if stock.symbol in self.stocks:
            raise InvalidOperation('Symbol {} already exists'.format(stock.symbol))
        self.stocks[stock.symbol] = stock
        stock.exchange = self

    def record_trade(self, symbol, quantity, buy_or_sell, price):
        # Validate values before creating a new key in self.trades
        trade = Trade(
            date_time=datetime.utcnow(),
            symbol=validate_member('symbol', symbol, self.stocks),
            quantity=validate_nonnegative('quantity', quantity),
            buy_or_sell=validate_member('buy_or_sell', buy_or_sell, ('buy', 'sell')),
            price=validate_nonnegative('price', price),
        )
        self.trades[symbol].append(trade)

    def all_share_index(self):
        """Calculate the all share index as the geometric mean of stock prices"""
        price_product = Decimal('1')
        for stock in self.stocks.values():
            price_product *= (stock.price() or 0)
        return price_product ** Decimal(1/len(self.stocks))

    def __str__(self):
        return self.name


class InvalidOperation(Exception):
    pass

