import os
import time
from binance.client import Client
from config import API_KEY, API_SECRET

# Initialize Binance Client for Testnet
client = Client(API_KEY, API_SECRET, testnet=True)

def get_account_info():
    """
    Fetch account balances from Binance Testnet
    """
    account = client.get_account()
    balances = account['balances']
    print("\nAccount Balances:")
    for b in balances:
        if float(b['free']) > 0:
            print(f"{b['asset']}: {b['free']}")
    return balances


def get_symbol_price(symbol="BTCUSDT"):
    """
    Fetch latest price of given trading pair
    """
    ticker = client.get_symbol_ticker(symbol=symbol)
    print(f"\nLatest Price of {symbol}: {ticker['price']}")
    return ticker
def get_historical_data(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, lookback="1 hour ago UTC"):
    """
    Fetch historical candlestick data from Binance Testnet.
    - symbol: trading pair (e.g., "BTCUSDT")
    - interval: timeframe (1m, 5m, 1h, 1d, etc.)
    - lookback: how much past data to fetch (e.g., "1 hour ago UTC", "1 day ago UTC")
    """
    import pandas as pd

    klines = client.get_historical_klines(symbol, interval, lookback)

    # Convert to DataFrame
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])

    # Keep only useful columns
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    print(f"\nFetched {len(df)} candlesticks for {symbol}")
    print(df.head())
    return df
def trading_loop(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE):
    """
    Simple trading loop:
    - Fetch latest candle
    - Get ML model signal (dummy logic for now)
    - Place BUY/SELL order on Testnet
    """
    print("\nStarting trading loop... (Press CTRL+C to stop)")

    while True:
        try:
            # Fetch latest candle
            klines = client.get_klines(symbol=symbol, interval=interval, limit=1)
            last_candle = klines[-1]
            close_price = float(last_candle[4])

            print(f"Latest {symbol} close price: {close_price}")

            # ===== Dummy ML model signal (replace with your real model later) =====
            # Example logic: if price ends with even digit → BUY, odd digit → SELL
            if int(close_price) % 2 == 0:
                signal = "BUY"
            else:
                signal = "SELL"
            print(f"Signal: {signal}")

            # ===== Place order on Testnet =====
            if signal == "BUY":
                order = client.create_order(
                    symbol=symbol,
                    side="BUY",
                    type="MARKET",
                    quantity=0.001  # test amount
                )
                print("✅ Buy order placed:", order["orderId"])

            elif signal == "SELL":
                order = client.create_order(
                    symbol=symbol,
                    side="SELL",
                    type="MARKET",
                    quantity=0.001  # test amount
                )
                print("✅ Sell order placed:", order["orderId"])

            # Wait before next check
            time.sleep(10)  # 10 seconds

        except Exception as e:
            print("Error in trading loop:", e)
            time.sleep(5)
def save_historical_data(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, lookback="1 day ago UTC", filename="data.csv"):
    """
    Fetch historical candlestick data and save it to CSV
    """
    import pandas as pd

    klines = client.get_historical_klines(symbol, interval, lookback)

    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])

    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Save to CSV
    df.to_csv(filename)
    print(f"\n✅ Saved {len(df)} rows to {filename}")

    return df
if __name__ == "__main__":
    get_account_info()
    get_symbol_price()
    # Save 7 days of 1-minute BTCUSDT data
    save_historical_data("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "7 days ago UTC", "btc_1min.csv")

