def place_buy_sell_order(ask_exchange_id, ask_price, bid_exchange_id, bid_price, symbol, amount):
    # buy
    ask_exchange = eval("ccxt.{0}()".format(ask_exchange_id))
    ask_exchange.apiKey = exchangesData[ask_exchange_id]["apiKey"]
    ask_exchange.secret = exchangesData[ask_exchange_id]["secret"]
    print("Placing a Buy order on {0} for {1} {2} at price: {3}".format(
        ask_exchange_id, amount, symbol.split("/")[0], ask_price))
    # It will cost you a fee if you want to use `create_market_buy_order`
    # ask_exchange.create_market_buy_order(symbol, amount, {'trading_agreement': 'agree'})
    ask_exchange.create_limit_buy_order(symbol, amount, ask_price)

    # sell
    bid_exchange = eval("ccxt.{0}()".format(bid_exchange_id))
    bid_exchange.apiKey = exchangesData[bid_exchange_id]["apiKey"]
    bid_exchange.secret = exchangesData[bid_exchange_id]["secret"]
    print("Placing a Sell order on {0} for {1} {2} at price: {3}".format(
        bid_exchange_id, amount, symbol.split("/")[0], bid_price))
    # It will cost you a fee if you want to use `create_market_buy_order`
    # bid_exchange.create_market_buy_order(symbol, amount, {'trading_agreement': 'agree'})
    bid_exchange.create_limit_sell_order(symbol, amount, bid_price)
