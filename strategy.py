import pandas
import numpy
import binance_connect
import time
import requests


# Function to conver data from binance candlestick data to a dataframe
def get_and_transform_data(symbol, timeframe, number_of_candle):
    raw_data = binance_connect.get_candlestick_data(
        symbol, timeframe, number_of_candle
    )
    print(f"Raw Data: {raw_data}")

    df = pandas.DataFrame(raw_data)
    df['time'] = pandas.to_datetime(df['time'], unit="ms")
    df['close_time'] = pandas.to_datetime(df['close_time'], unit="ms")
    df["RedOrGreen"] = numpy.where((df["open"] < df["close"]), "Green", "Red")

    return df


# Get the token price
def get_token_price(address, chain):
    # Make an API call to get the price
    url = f"http://localhost:5002/getPrice?address={address}&chain={chain}"
    response = requests.get(url)
    data = response.json()

    # Extract the price
    usd_price = data["usdPrice"]
    return usd_price


# Check the pare relation
def check_pair_relation(address1, address2, chain):
    price1 = get_token_price(address1, chain)
    price2 = get_token_price(address2, chain)

    # Calculate ratio of the prices
    ratio = price1 / price2
    return ratio


def check_ratio_ratio_relation(current_ratio, reference_ratio):
    # Calculate the difference between the ratios
    # Ratio 1 = TOKEN1/TOKEN3
    # Ratio 2 = TOKEN3/TOKEN3
    if current_ratio > reference_ratio:
        # The current ratio is overvalued relative to the reference ratio
        # Consider Selling TOKEN1 for TOKEN3
        return False
    elif current_ratio < reference_ratio:
        # The current ratio is undervalued relative to the reference ratio
        # Consider Buying TOKEN1 with TOKEN3
        return True


# Function to check the consecutive raise or decrease
def determine_trade_event(symbol, timeframe, percent_change, candle_color):
    candlestick_data = get_and_transform_data(symbol, timeframe, 3)
    # Review if the candle has the same color
    if (
        candlestick_data.loc[0, "RedOrGreen"] == candle_color
        and candlestick_data.loc[1, "RedOrGreen"] == candle_color
        and candlestick_data.loc[2, "RedOrGreen"] == candle_color
    ):
        # Determine the percentage change
        change_one = determine_percentage_change(
            candlestick_data.loc[0, "open"], candlestick_data.loc[0, "close"]
        )
        change_two = determine_percentage_change(
            candlestick_data.loc[1, "open"], candlestick_data.loc[1, "close"]
        )
        change_three = determine_percentage_change(
            candlestick_data.loc[2, "open"], candlestick_data.loc[2, "close"]
        )

        if candle_color == "Red":
            print(f"First Drop: {change_one}")
            print(f"Second Drop: {change_two}")
            print(f"Third Drop: {change_three}")
        elif candle_color == "Green":
            print(f"First Increase: {change_one}")
            print(f"Second Increase: {change_two}")
            print(f"Third Increase: {change_three}")

        # Compare the price changes against stated percentage change

        # The minimum treshold of increase or decrease we want to see in the price
        # in order to make the sell/buy decision
        if (change_one >= percent_change and change_two >= percent_change and change_three >= percent_change):
            # Wecan trade
            return True
        else:
            # We can not trade
            return False
    else:
        # We can not trade
        return False


def determine_percentage_change(close_previous, close_current):
    return (close_current - close_previous) / close_previous


def analyze_symbols(symbol_dataframe, timeframe, percentage, type):
    # print(f"symbol_dataframe: {symbol_dataframe}")
    # Iterate through all the symbols
    for index in symbol_dataframe.index:
        # Analize symbol
        if type == "buy":
            analysis = determine_trade_event(
                symbol_dataframe.loc[index],
                timeframe,
                percentage,
                "Green"
            )
            
            print(f"analysis: {analysis}")

            if analysis:
                print(
                    f'{symbol_dataframe["symbol"]["index"]} has 3 consecutive rises')
            else:
                print(
                    f'{symbol_dataframe["symbol"]["index"]} does not have 3 consecutive rises')

            # Sleep 1
            time.sleep(1)
            return analysis

        elif type == "sell":
            analysis = determine_trade_event(
                symbol_dataframe.loc[index],
                timeframe,
                percentage,
                "Red"
            )

            if analysis:
                print(
                    f'{symbol_dataframe["symbol"]["index"]} has 3 consecutive drops')
            else:
                print(
                    f'{symbol_dataframe["symbol"]["index"]} does not have 3 consecutive drops')

            # Sleep 1
            time.sleep(1)
            return analysis
