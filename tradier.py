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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, type=str)
    parser.add_argument("--side", required=True, type=str)
    parser.add_argument("--quantity", required=False, type=str, default="1")
    parser.add_argument("--duration", required=False, type=str, default="day")
    parser.add_argument("--type", required=False, type=str, default="market")
    parser.add_argument("--price", required=False, type=str, default=None)
    
    args = parser.parse_args()

    symbol = args.symbol
    side = args.side
    quantity = args.quantity
    duration = args.duration
    type = args.type
    price = args.price
    
    print(symbol, side, quantity, duration, type, price)
    
    tradier = Tradier(AUTH_TOKEN)
    profile = tradier.get_user_profile()
    for account in profile["profile"]["account"]:
        account_id = account["account_number"]
        try:
            resp = tradier.equity_order(account_id, symbol, side, quantity, duration, type, price)
            print(resp)
        except Exception as e:
            print(e)
        time.sleep(0.6)
    
    
if __name__ == "__main__":
    main()