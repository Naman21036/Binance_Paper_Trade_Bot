from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
BASE_ORDER_USDT = float(os.getenv("BASE_ORDER_USDT", "10"))
TESTNET = os.getenv("TESTNET", "true").lower() in ("true","1","yes")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() in ("true","1","yes")
KLINE_INTERVAL = os.getenv("KLINE_INTERVAL", "1m")
KLINE_LIMIT = int(os.getenv("KLINE_LIMIT", "200"))
SLEEP_SECONDS = int(os.getenv("SLEEP_SECONDS", "60"))
