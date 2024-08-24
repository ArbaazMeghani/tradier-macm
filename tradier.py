import requests
import time
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("TRADIER_AUTH_TOKEN")

class Tradier:
    def __init__(self, auth_token):
        self.base_url = "https://api.tradier.com/v1"
        self.auth_token = auth_token
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        
    def get_user_profile(self):
        url = f"{self.base_url}/user/profile"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_positions(self, account_id):
        url = f"{self.base_url}/accounts/{account_id}/positions"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def equity_order(self, account_id, symbol, side, quantity = "1", duration = "day", type = "market", price = None):
        if type == "limit" and price is None:
            raise ValueError("Price must be provided for limit orders")
        if type == "market" and price is not None:
            raise ValueError("Price should not be provided for market orders")
        if side not in ["buy", "sell"]:
            raise ValueError("Side must be either 'buy' or 'sell'")
        if type not in ["market", "limit"]:
            raise ValueError("Type must be either 'market' or 'limit'")
        if duration not in ["day", "gtc", "pre", "post"]:
            raise ValueError("Duration must be either 'day', 'gtc', 'pre', or 'post'")
        if duration in ["gtc", "pre", "post"] and type == "market":
            raise ValueError("GTC orders cannot be market orders")
        
        
        url = f"{self.base_url}/accounts/{account_id}/orders"
        payload = {
            "class": "equity",
            "symbol": symbol,
            "quantity": quantity,
            "side": side,
            "type": type,
            "duration": duration,
        }
        
        if type == "limit":
            payload["price"] = price
        
        response = requests.post(url, headers=self.headers, data=payload)
        response.raise_for_status()
        return response.json()

def print_help():
    print("Usage: python tradier.py --symbol [SYMBOL] --side [SIDE] --quantity [QUANTITY] --duration [DURATION] --type [TYPE] --price [PRICE] --check")
    print("[Required] SYMBOL: the stock symbol")
    print("[Required] SIDE: buy or sell")
    print("[Optional, default: day] DURATION: day, gtc [limit required], pre [limit required], post [limit required]")
    print("[Optional, default: market] TYPE:  market or limit")
    print("PRICE: required for limit orders, not required for market orders")
    print("[Optional, default: no check] CHECK: only buy if you don't already have a position")
    print("[Optional, default: 1] Quantity: Num shares to buy/sell")

def check_positions(tradier, account_id, symbol):
    positions = tradier.get_positions(account_id)
    if "positions" not in positions:
        return False
    if "position" not in positions["positions"]:
        return False
    if not isinstance(positions["positions"]["position"], list):
        positions["positions"]["position"] = [positions["positions"]["position"]]

    for position in positions["positions"]["position"]:
        if position["symbol"] == symbol:
            print(f"{account_id} already has a position in {symbol}")
            return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--usage", required=False, action="store_true")
    parser.add_argument("--symbol", required=False, type=str)
    parser.add_argument("--side", required=False, type=str)
    parser.add_argument("--quantity", required=False, type=str, default="1")
    parser.add_argument("--duration", required=False, type=str, default="day")
    parser.add_argument("--type", required=False, type=str, default="market")
    parser.add_argument("--price", required=False, type=str, default=None)
    parser.add_argument("--check", required=False, action="store_true")
    
    args = parser.parse_args()
    help = args.usage
    symbol = args.symbol
    side = args.side
    quantity = args.quantity
    duration = args.duration
    type = args.type
    price = args.price
    check = args.check
    
    if symbol:
        symbol = symbol.upper()
    
    if help:
        print_help()
        return
    
    print(f"Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Duration: {duration}, Type: {type}, Price: {price}, Check: {check}")
    
    tradier = Tradier(AUTH_TOKEN)
    profile = tradier.get_user_profile()
    for account in profile["profile"]["account"]:
        account_id = account["account_number"]
        has_position = False
        if check:
            has_position = check_positions(tradier, account_id, symbol)
        
        if check and has_position:
            continue
        
        try:
            resp = tradier.equity_order(account_id, symbol, side, quantity, duration, type, price)
            print(f"{account_id}: {resp}")
        except Exception as e:
            print(f"{account_id}: error - {e}")
        time.sleep(0.6)
    
    
if __name__ == "__main__":
    main()