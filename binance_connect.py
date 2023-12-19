from binance.spot import Spot
import pandas


# Function to get the status
def query_binance_status():
    status = Spot().system_status()
    if status['status'] == 0:
        return True
    else:
        raise ConnectionError


# Function query account
def query_account(api_key, api_secret, base_url):
    return Spot(
        api_key=api_key,
        api_secret=api_secret,
        base_url=base_url
    ).account()


# Query testnet
def query_testnet(base_url):
    client = Spot(base_url=base_url)
    print(client.time())


# Function to query candlestick data
def get_candlestick_data(symbol, timeframe, qty):
    # Get raw data
    raw_data = Spot().klines(symbol=symbol, interval=timeframe, limit=qty)
    converted_data = []

    for candle in raw_data:
        converted_candle = {
            "time": candle[0],
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
            "close_time": candle[6],
            "quote_asset_volume": float(candle[7]),
            "number_of_trades": int(candle[8]),
            "taker_buy_base_assets_volume": float(candle[9]),
            "taker_buy_quote_assets_volume": float(candle[10]),
        }

        # Add the data
        converted_data.append(converted_candle)
    return converted_data


# Function to query all symbols from base asset
def query_quote_assets_list(quote_asset_symbol):
    symbole_dictionary = Spot().exchange_info()
    # conver this into dataframe
    symbol_dataframe = pandas.DataFrame(symbole_dictionary["symbols"])
    # Extract all the symbols with the base asset pair (ETH)
    quote_symbol_dataframe = symbol_dataframe.loc[
        symbol_dataframe["quoteAsset"] == quote_asset_symbol
    ]
    quote_symbol_dataframe = symbol_dataframe.loc[
        symbol_dataframe["status"] == "TRADING"
    ]

    return quote_symbol_dataframe


# Function to make trade with params
def make_trade_with_params(api_key, api_secret, base_url, params):
    print("Making trade with params")
    client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)

    try:
        response = client.new_order(**params)
        return response
    except ConnectionRefusedError as error:
        print(f"Error: {error}")


# Function to query trades
def query_open_trades(api_key, api_secret, base_url, params):
    client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)
    # get trades
    try:
        response = client.get_open_orders()
        return response
    except ConnectionRefusedError as error:
        print(f"Error: {error}")


# Function to cancel a trade
def cancel_order_by_symbol(api_key, api_secret, base_url, symbol):
    client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)

    # Cancel the trade
    try:
        response = client.cancel_open_orders(symbol=symbol)
        return response
    except ConnectionRefusedError as error:
        print(f"Error: {error}")


# Function to place a limit order for symbol
def place_limit_order(api_key, api_secret, base_url, symbol, side, quantity, price):
    client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)

    # Place the limit order
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            TimeoutError="GTC",
            quantity=quantity,
            price=price
        )
        return response
    except ConnectionRefusedError as error:
        print(f"Error: {error}")


# Place stop loss order
def place_stop_loss_order(api_key, api_secret, base_url, symbol, side, quantity, stop_price, limit_price):
    client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)

    # Place the limit order
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="STOP_LOSS_LIMIT",
            TimeoutError="GTC",
            quantity=quantity,
            stop_price=stop_price,
            price=limit_price
        )
        return response
    except ConnectionRefusedError as error:
        print(f"Error: {error}")


# Place take profit order
def take_profit_order(api_key, api_secret, base_url, symbol, side, quantity, stop_price, limit_price):
    client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)

    # Place the take profit order
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="TAKE_PROFIT_LIMIT",
            TimeoutError="GTC",
            quantity=quantity,
            stop_price=stop_price,
            price=limit_price
        )
        return response
    except ConnectionRefusedError as error:
        print(f"Error: {error}")
