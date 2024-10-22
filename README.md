# Tradier-MACM

## Prerequisites
1. Python 3


## Getting your Tradier token
1. Login to tradier
2. Click on your profile
3. Go to "API Access"
4. Generate access token under production account access
5. Copy your token

## Install
1. Run
`pip install -r requirements.txt`
2. Rename sample.env to .env
3. Replace <YOUR_TOKEN> with your Tradier token

## Usage
- Help Menu: `python tradier.py --usage`
- Order: `--symbol [SYMBOL] --side [SIDE] --quantity [QUANTITY] --duration [DURATION] --type [TYPE] --price [PRICE] --check"`

## Options
- [Required] SYMBOL: the stock symbol
- [Required] SIDE: `buy` or `sell`
- [Optional, default: day] DURATION: `day`, `gtc` [limit required], `pre` [limit required], `post` [limit required]
- [Optional, default: market] TYPE: `market` or `limit`
- [Optional, default: no check] CHECK: only buy if you don't already have a position
- [Optional, default: 1] Quantity: Number of shares to buy/sell
- PRICE: required for limit orders, not required for market orders. Optionally, you can use `auto` for the price. It will use ask+0.10 for buy orders and bid-0.10 for sell orders