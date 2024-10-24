from interactions import slash_command, slash_option, OptionType, SlashCommandChoice, SlashContext, Embed, Client
import os
import time
from dotenv import load_dotenv
from tradier import Tradier, check_positions

load_dotenv()

AUTH_TOKEN = os.getenv("TRADIER_AUTH_TOKEN")
bot = Client(token=os.getenv("DISCORD_BOT_TOKEN"))

@slash_command(name="trade", description="Trade on tradier")
@slash_option(
    name="symbol",
    description="Stock Symbol",
    required=True,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="side",
    description="Buy or Sell",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Buy", value='buy'),
        SlashCommandChoice(name="Sell", value='sell')
    ]
)
@slash_option(
    name="type",
    description="Order Type, defaults to market",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Market", value='market'),
        SlashCommandChoice(name="Limit", value='limit'),
    ]
)
@slash_option(
    name="duration",
    description="Order duration, defaults to day",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Day", value='day'),
        SlashCommandChoice(name="Premarket", value='pre'),
        SlashCommandChoice(name="Postmarket", value='post'),
        SlashCommandChoice(name="Good-Till-Cancelled", value='gtc'),
    ]
)
@slash_option(
    name="price",
    description="Limit Price, only valid for limit orders. use auto for automatic pricing",
    required=False,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="quantity",
    description="Order quantity, defaults to 1",
    required=False,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="check",
    description="Check if symbol is already owned, valid for buy orders only",
    required=False,
    opt_type=OptionType.BOOLEAN,
)
async def trade(ctx: SlashContext, symbol: str, side: str, type: str = 'market', duration: str = 'day', price: str = None, quantity: str = "1", check: bool = False):
    try:
        await ctx.defer()
        
        if symbol:
            symbol = symbol.upper()
        if side:
            side = side.lower()
        if duration:
            duration = duration.lower()
        if type:
            type = type.lower()
        if price:
            price = price.lower()
        
        if side == "sell" and check:
            await ctx.send("Cannot check for positions when selling")
            return
        
        await ctx.send(f"Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Duration: {duration}, Type: {type}, Price: {price}, Check: {check}")
        
        tradier = Tradier(AUTH_TOKEN)
        profile = tradier.get_user_profile()
        
        if price == "auto":
            price = tradier.get_auto_price(symbol, side)
            await ctx.send(f"Auto Limit Price: {price}")

        for account in profile["profile"]["account"]:
            account_id = account["account_number"]
            has_position = False
            if check:
                has_position = check_positions(tradier, account_id, symbol)
            
            if check and has_position:
                await ctx.send(f"{account_id} already has a position in {symbol}")
                continue
            
            try:
                resp = tradier.equity_order(account_id, symbol, side, quantity, duration, type, price)
                await ctx.send(f"{account_id}: {resp}")
            except Exception as e:
                await ctx.send(f"{account_id}: error - {e}")
            time.sleep(1.1 if check else 0.6)
    except Exception as e:
        await ctx.send("Something went wrong: {e}")


bot.start()