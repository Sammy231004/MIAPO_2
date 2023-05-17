
def get_biggest_spread_by_symbol(exchanges, symbol):
    ask_exchange_id = ""
    min_ask_price = 99999999

    bid_exchange_id = ""
    max_bid_price = 0

    for exchange_id in exchanges:
        exchange = eval("ccxt.{0}()".format(exchange_id))

        try:
            order_book = exchange.fetch_order_book(symbol)
            bid_price = order_book['bids'][0][0] if len(
                order_book['bids']) > 0 else None
            ask_price = order_book['asks'][0][0] if len(
                order_book['asks']) > 0 else None

            if ask_price < min_ask_price:
                ask_exchange_id = exchange_id
                min_ask_price = ask_price
            if bid_price > max_bid_price:
                bid_exchange_id = exchange_id
                max_bid_price = bid_price

            increase_percentage = (bid_price - ask_price) / ask_price * 100
            if increase_percentage >= 1:
                return ask_exchange_id, min_ask_price, bid_exchange_id, max_bid_price
        except:
            # pass
            print("")
            print("{0} - There is an error!".format(exchange_id))

    min_ask_price += 0.235
    max_bid_price -= 0.235

    return ask_exchange_id, min_ask_price, bid_exchange_id, max_bid_price
