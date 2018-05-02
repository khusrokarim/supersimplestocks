from decimal import Decimal

def validate_nonnegative(name, value, allow_none=False):
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

