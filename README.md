# Super Simple Stocks

This is a Python 3.5+ implementation of Super Simple Stocks.

## Implementation details

All logic is contained within super\_simple\_stocks.py, held in two classes.

### Stock

This class represents a single stock.  It is constructed using 3 positional arguments and 2 keyword arguments:

    Stock(symbol, stock_type, par_value, last_dividend=None, fixed_dividend=None)

Stock objects contain the following attributes:

 * exchange
 * dividend\_yield
 * pe\_ratio
 * price
 * record\_trade(quantity, buy\_or\_sell, price)


### Exchange

This class represents an exchange, which operates on a number of stocks.  It is constructed by passing a string to represent the name.

The Exchange class contains a single class-level method, load\_stocks(json\_filename).

Exchange objects contain the following attributes:

 * stocks
 * trades
 * all\_share\_index
 * record\_trade(symbol, quantity, buy\_or\_sell, price)
 * add\_stock(stock)

## Assumptions

I have assumed that:
 * All stocks are required to have exactly one symbol, a type, and a par value.
 * Within a single exchange, a symbol uniquely identifies a stock.
 * A stock type must be either 'common' or 'preferred'.  This list is easily extended.
 * Each stock is traded on a a maximum of one exchange.
 * All prices and dividends must be positive.

I have not assumed that:
 * Prices must always be in a whole number of pennies.  Adopting this assumption, if it is valid, would improve performance.
