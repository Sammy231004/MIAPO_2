def main():
    exchanges = [
        "binance",
        "bittrex",
        "poloniex",
        "bybit",
        "kucoin",
    ]


    markets = []
    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()
        exchange.load_markets()
        markets += [market for market in exchange.markets if 'USDT' in market]

    symbols = list(set(markets))

    min_ask_exchange_id = ""
    min_ask_price = 99999999

    max_bid_exchange_id = ""
    max_bid_price = 0

    exchange_symbol = ""
    max_increase_percentage = 0.0

    for symbol in symbols:
        print("-----------------------------")
        print("Searching for the best opportunity for {0} on {1}".format(
            symbol, exchanges))

        ask_exchange_id, ask_price, bid_exchange_id, bid_price = get_biggest_spread_by_symbol(
            exchanges, symbol)
        increase_percentage = (bid_price - ask_price) / ask_price * 100

        print("[{0} - {1}] - [{2}] - Price Spread: {3:.2}%".format(ask_exchange_id,
                                                                   bid_exchange_id, symbol, increase_percentage))

        if increase_percentage > max_increase_percentage:
            exchange_symbol = symbol
            max_increase_percentage = increase_percentage
            min_ask_exchange_id = ask_exchange_id
            min_ask_price = ask_price
            max_bid_exchange_id = bid_exchange_id
            max_bid_price = bid_price

        if increase_percentage >= min_spread:
            break
    print("-----------------------------")

    if max_increase_percentage > 0:
        print("\n----------Settings-----------")
        ask_amount = get_min_amount(min_ask_exchange_id, exchange_symbol)
        print("Min Ask amount: {0}".format(ask_amount))
        bid_amount = get_min_amount(max_bid_exchange_id, exchange_symbol)
        print("Min Bid amount: {0}".format(bid_amount))
        amount = max(ask_amount, bid_amount)
        print("Actual amount: {0}".format(amount))
        print("Min spread percentage: {0}%".format(min_spread))
        print("Min profit: {0}%".format(min_profit))

        print("\n--------Best Spread----------")
        print("[{0} - {1}] - [{2}]: Spread percentage: {3:.2}%".format(min_ask_exchange_id,
                                                                       max_bid_exchange_id, exchange_symbol, max_increase_percentage))

        print("\n-----Market Opportunity------")
        print("Buy {0} {1} from {2} at {3} {4}".format(amount, exchange_symbol.split(
            "/")[0], min_ask_exchange_id, min_ask_price, exchange_symbol.split("/")[0]))
        print("Sell {0} {1} on {2} at {3} {4}".format(amount, exchange_symbol.split(
            "/")[0], max_bid_exchange_id, max_bid_price, exchange_symbol.split("/")[0]))

        print("\n-------------Fees------------")
        min_ask_fee = min_ask_price * amount * \
            exchangesData[min_ask_exchange_id]["transactionFee"]
        print("[{0}] - Trading Fee: {1}% = {2:.4} {3}".format(min_ask_exchange_id,
                                                              exchangesData[min_ask_exchange_id]["transactionFee"]*100, min_ask_fee, exchange_symbol.split("/")[0]))
        max_bid_fee = max_bid_price * amount * \
            exchangesData[max_bid_exchange_id]["transactionFee"]
        print("[{0}] - Trading Fee: {1}% = {2:.4} {3}".format(max_bid_exchange_id,
                                                              exchangesData[max_bid_exchange_id]["transactionFee"]*100, max_bid_fee, exchange_symbol.split("/")[0]))

        print("\n-----------Profit------------")
        cost = amount * min_ask_price
        print("You will have to spend: {0:.4} {1}".format(
            cost, exchange_symbol.split("/")[1]))
        profit = ((max_bid_price - min_ask_price) * amount) - \
            (max_bid_fee + min_ask_fee)
        print("You will make {0:.4} {1} profit(including fees)".format(
            profit, exchange_symbol.split("/")[1]))

        print("\n-----------Buy/Sell----------")
        if profit >= min_profit:
            place_buy_sell_order(min_ask_exchange_id, min_ask_price,
                                 max_bid_exchange_id, max_bid_price, exchange_symbol, amount)
        else:
            print("It seems like you won't make enough profit :(")
    else:
        print("It seems like there are no opportunities at the moment :(")
