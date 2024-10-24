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

## Running Discord Bot
1. Create a Discord server
2. Login to Discord Developers Site https://discord.com/developers/applications
3. Click create new application and follow the steps to make a new application.
4. Go to the installation tab
5. Under install link, select none
6. Go to the bot tab
7. Reset the token and copy it
8. Replace `<BOT_TOKEN>` in the .env file with the copied token
9. Back in the bot tab, scroll down and make sure public bot is disabled
10. Go to the Oauth2 tab
11. In URL Generator select `bot` and select `application.commands`
12. Scroll down and copy the generated URL
13. Paste it in a new tab to invite the bot into your discord server
14. In Pycharm, you can run the `bot.py` file to start the discord bot
15. Then in your discord server, you should be able to place trades using the `/trade` command