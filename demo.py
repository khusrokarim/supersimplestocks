import random
from decimal import Decimal

from super_simple_stocks import Stock, Exchange, Trade, InvalidOperation

def demo():
    stocks = (
        Stock('TEA', 'common', 100, 0),
        Stock('POP', 'common', 100, 8),
        Stock('ALE', 'common', 60, 23),
        Stock('GIN', 'preferred', 100, 8, 0.02),
        Stock('JOE', 'common', 250, 13),
    )
    exchange = Exchange('GBCE')
    print('Created exchange {}'.format(exchange))
    for stock in stocks:
        exchange.add_stock(stock)
        print('Added {} to {}'.format(stock, exchange))
    print('Recording 10 random trades:')
    for _ in range(10):
        stock = random.choice(stocks)
        buy_or_sell = random.choice(('buy', 'sell'))
        quantity = random.randint(1, 1000)
        price = random.randint(1, 1000)
        stock.record_trade(quantity, buy_or_sell, price)
        print('   {}'.format(exchange.trades[stock.symbol][-1]))
    for stock in stocks:
        print('-----')
        print(stock.symbol)
        try:
            print('Dividend yield: {}'.format(stock.dividend_yield()))
        except InvalidOperation:
            pass
        try:
            print('P/E Ratio: {}'.format(stock.pe_ratio()))
        except InvalidOperation:
            pass
        print('Price: {}'.format(stock.price()))
    print('-----')
    print('GBCE All-Share Index: {}'.format(exchange.all_share_index()))

if __name__ == '__main__':
    demo()
