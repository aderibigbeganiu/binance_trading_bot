import json
import binance_connect
import environ
import strategy

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()


if __name__ == "__main__":
    base_url = env("BINANCE_BASE_URL")
    api_key = env("BINANCE_API_KEY")
    api_secret = env("BINANCE_SECRET_KEY")
    BUSD = env("BINANCE_BUSD_TOKEN")
    ETH = env("BINANCE_ETH_TOKEN")
    BTC = env("BINANCE_BTCB_TOKEN")
    LTC = env("BINANCE_LTC_TOKEN")

    account = binance_connect.query_account(api_key, api_secret, base_url)
    if account["canTrade"]:
        print("Your account is ready to trade")

        # Calculate the current ratio
        reference_ratio = strategy.check_pair_relation(ETH, LTC, "bsc")
        current_ratio = strategy.check_pair_relation(BUSD, LTC, "bsc")

        # Calculate the differences between ratio
        check = strategy.check_ratio_ratio_relation(
            current_ratio,
            reference_ratio
        )
        asset_list = binance_connect.query_quote_assets_list("LTC")
        eth_pair = asset_list.loc[asset_list["symbol"] == "LTCETH"]
        symbol = eth_pair["symbol"].values[0]
        if check:
            print("Buying time")
            analysis = strategy.analyze_symbols(
                eth_pair, '1h', 0.0001, "buy")
            if analysis:
                print("Buying ETH")
            else:
                print("Not buying ETH")
                print(f"Reason: The analysis is {analysis}")
        else:
            print("Selling time")
            analysis = strategy.analyze_symbols(
                eth_pair, '1h', 0.000001, "sell")
            if analysis:
                print("Selling ETH")
            else:
                print("Not selling ETH")
                print(f"Reason: The analysis is {analysis}")
