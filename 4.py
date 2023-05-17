
def get_exchanges_by_symbol(exchanges, symbol_to_find):
    for exchange_id in exchanges:
        exchange = eval("ccxt.{0}()".format(exchange_id))

        exchange.load_markets(True)

        for symbol in exchange.symbols:
            if symbol == symbol_to_find:
                print("{0} - {1} [OK]".format(exchange_id, symbol))