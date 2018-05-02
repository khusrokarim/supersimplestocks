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


class Stock:
    """A single stock, optionally traded on a single exchange."""

    stock_types = (
        'common',
        'preferred',
    )

    def __init__(self, symbol, stock_type, par_value, last_dividend=None, fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = stock_type
        self.par_value = as_nonnegative_decimal('par_value', par_value)
        self.last_dividend = as_nonnegative_decimal('last_dividend', last_dividend, True)
        self.fixed_dividend = as_nonnegative_decimal('fixed_dividend', fixed_dividend, True)
        self.exchange = None

    @property
    def stock_type(self):
        return self._stock_type

    @stock_type.setter
    def stock_type(self, value):
        if value not in self.stock_types:
            raise ValueError('stock_type must be one of {} (received {})'.format(self.stock_types, value))
        self._stock_type = value

    @property
    def fixed_dividend(self):
        return self._fixed_dividend

    @fixed_dividend.setter
    def fixed_dividend(self, value):
        if (self.stock_type == 'preferred') and (value is None):
            raise TypeError('Preferred stock must have a fixed dividend')
        self._fixed_dividend = value


class Exchange:
    """A stock exchange for trading individual Stocks."""

    def __init__(self, name):
        self.name = name
