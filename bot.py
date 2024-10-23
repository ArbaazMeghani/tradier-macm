from interactions import slash_command, slash_option, OptionType, SlashCommandChoice, SlashContext, Embed, Client
import os
from dotenv import load_dotenv

load_dotenv()


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
        
        await ctx.send("test")
        await ctx.followup.send("test")
    except Exception as e:
        await ctx.send("Something went wrong, try again")


bot.start()