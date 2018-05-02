from collections import defaultdict, namedtuple
from datetime import datetime, timedelta
from decimal import Decimal

def as_nonnegative_decimal(name, value, allow_none=False):
    """
    Validate that `value` is a non-negative number, in a representation accepted by Decimal().
    Returns `value` as a Decimal, or None if `allow_none` is True and `value` is None.
    Raises ValueError if `value` is negative.
    """

    if value is None:
        if allow_none:
            return None
        raise TypeError('{} must be a non-negative number (received {})'.format(name, value))
    elif value < 0:
        raise ValueError('{} must not be negative (received {})'.format(name, value))
    else:
        return Decimal(value)

def validate_member(name, value, permitted):
    if value not in permitted:
        raise ValueError('{} must be one of {} (received {})'.format(name, permitted, value))
    return value


Trade = namedtuple('Trade', ['date_time', 'symbol', 'quantity', 'buy_or_sell', 'price'])

class InvalidOperation(Exception):
    pass


class Stock:
    """A single stock, optionally traded on a single exchange."""

    stock_types = (
        'common',
        'preferred',
    )

    def __init__(self, symbol, stock_type, par_value, last_dividend=Decimal(), fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = validate_member('stock_type', stock_type, self.stock_types)
        self.par_value = as_nonnegative_decimal('par_value', par_value)
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
        if not self.last_dividend:
            raise InvalidOperation((
                'P/E ratio cannot be calculated for {} '
                'because it has not distributed a dividend'
            ).format(self.symbol))
        return self.price() / self.last_dividend

    @property
    def last_dividend(self):
        return self._last_dividend

    @last_dividend.setter
    def last_dividend(self, value):
        self._last_dividend = as_nonnegative_decimal('last_dividend', value)

    @property
    def fixed_dividend(self):
        """Fixed dividend.  Required for preferred stocks."""
        return self._fixed_dividend

    @fixed_dividend.setter
    def fixed_dividend(self, value):
        if (self.stock_type == 'preferred') and (value is None):
            raise TypeError('Preferred stock must have a fixed dividend')
        self._fixed_dividend = as_nonnegative_decimal('fixed_dividend', value, True)

    @property
    def exchange(self):
        """The exchange associated with this stock"""
        try:
            return self._exchange
        except AttributeError:
            raise InvalidOperation("Stock {} is not associated with an exchange".format(self.symbol))

    @exchange.setter
    def exchange(self, value):
        self._exchange = value


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
            quantity=as_nonnegative_decimal('quantity', quantity),
            buy_or_sell=validate_member('buy_or_sell', buy_or_sell, ('buy', 'sell')),
            price=as_nonnegative_decimal('price', price),
        )
        self.trades[symbol].append(trade)
