from Robinhood import Robinhood

robinhood_client = Robinhood()

robinhood_client.login(username='username', password='password')

def get_owned_list():
    return robinhood_client.securities_owned()['results']

def get_symbol(url = None):
    return robinhood_client.get_stock_info(url)['symbol']

def get_current_price(symbol):
    stock_instrument = robinhood_client.instruments(symbol)[0]
    # Get a stock's quote
    stock_quote = robinhood_client.quote_data(symbol)
    return stock_quote['last_trade_price']

def compute_stop_price(current_price):
    res = float(current_price) * 0.984
    return round(res, 2)

def place_stop_loss_order(ins, symbol, stop_price, quantity):
    # GFD: good for day
    # GTC: good till canceled
    order = robinhood_client.my_place_stop_loss_sell_order(ins, symbol, 'GFD', stop_price, quantity)


for owned in get_owned_list():
    # Get instrument
    ins = owned['instrument']
    symbol = get_symbol(ins)
    quantity = float(owned['quantity'])
    current_price = get_current_price(symbol)
    print("current_price = " + str(current_price))

    print(str(ins) + ' ' + str(symbol) + ' ' + str(current_price) + ' ' + str(quantity))

    place_stop_loss_order(ins, symbol, compute_stop_price(current_price), quantity)


