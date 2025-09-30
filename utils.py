import math

# Round quantity down to match Binance lot size rules
def round_down(quantity, step_size):
    """
    Rounds quantity down to nearest step_size.
    Example: round_down(5.678, 0.01) -> 5.67
    """
    return math.floor(quantity / step_size) * step_size


# Calculate position size based on risk percentage
def calculate_position_size(balance, risk_percent, price):
    """
    Example: If balance=1000, risk=1%, price=50
    -> position size = (1000 * 0.01) / 50 = 0.2 units
    """
    risk_amount = balance * (risk_percent / 100)
    return risk_amount / price


# Pretty print order response
def print_order_response(order):
    """
    Makes Binance API order response easier to read
    """
    print("\nOrder Executed:")
    print(f"Symbol: {order['symbol']}")
    print(f"Side: {order['side']}")
    print(f"Status: {order['status']}")
    print(f"Executed Qty: {order['executedQty']}")
    print(f"Price: {order['fills'][0]['price'] if order['fills'] else 'N/A'}")
