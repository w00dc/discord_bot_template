import asyncio
import json
import os
import logging
import platform
import discord
import random
import re
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from config import get_settings, LoggingFormatter

# Setup bot intents (events restrictions)
# For more information about intents, please go to the following websites:
# https://discordpy.readthedocs.io/en/latest/intents.html
# https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


# Default Intents:
# intents.bans = True
# intents.dm_messages = True
# intents.dm_reactions = True
# intents.dm_typing = True
# intents.emojis = True
# intents.emojis_and_stickers = True
# intents.guild_messages = True
# intents.guild_reactions = True
# intents.guild_scheduled_events = True
# intents.guild_typing = True
# intents.guilds = True
# intents.integrations = True
# intents.invites = True
# intents.messages = True # `message_content` is required to get the content of the messages
# intents.reactions = True
# intents.typing = True
# intents.voice_states = True
# intents.webhooks = True

# Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
# intents.members = True
# intents.message_content = True
# intents.presences = True

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

settings = get_settings()

bot = Bot(
    command_prefix=commands.when_mentioned_or(settings.cmd_prefix),
    intents=intents,
    # help_command=None,
)

# Setup the loggers; Give the logger the bot's name
logger = logging.getLogger(settings.bot_name)
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")
    if settings.sync_commands_globally:
        bot.logger.info("Syncing commands globally...")
        await bot.tree.sync()


@bot.command(name="greet", help="Get an emoji greeting!")
async def greeting(ctx):
    emojis = [
        ":poop:",
        ":wave:",
        ":+1:",
    ]

    response = random.choice(emojis)
    bot.logger.info(f"Responding to {ctx.author.name} with a {response}")
    await ctx.send(response)


@bot.command(name="roll", help="Simulates rolling dice returning the total")
async def roll(
    ctx,
    dice_str: str = commands.parameter(
        description="Valid dice roll string with +/- mod and NO SPACES -- ie, 2d8+1 for 2 x 8-sided dice + 1"
    ),
):
    # Pull any Mod out of the string
    mod = 0
    mod_op = "+"
    dice_str_raw = dice_str
    if "+" in dice_str or "-" in dice_str:
        dice_and_mod = re.split("[-\+]+", dice_str)
        dice_str_raw = dice_and_mod[0]
        mod_op = re.findall("[-\+]+", dice_str)[0]
        mod = dice_and_mod[-1]
    # Split string into Num of Dice and Dice Sides
    sides_and_dice = dice_str_raw.split("d")
    if len(sides_and_dice) != 2 or any(not n.isnumeric() for n in sides_and_dice):
        bot.logger.error(f"{dice_str} is not a valid format for the roll command")
        await ctx.send(f"**{dice_str}** is not a valid format for the roll command")
        return
    sides = int(sides_and_dice[1])
    dice = int(sides_and_dice[0])
    roll = 0
    inv_rolls = []
    # Sum up the sides while keeping track of the individual rolls
    for i in range(dice):
        inv_rolls.append(random.choice(range(1, sides + 1)))
        roll += inv_rolls[-1]
    # Evaluate the mod
    roll = eval(f"roll {mod_op} {mod}")
    # Null out vars if mod is zero
    if mod == 0:
        mod_op = ""
        mod = ""
    # Log and return output as a message
    bot.logger.info(
        f"Rolling a {dice}d{sides}{mod_op}{mod} for {ctx.author.name}  ⟶  {roll}   ( {inv_rolls}{mod_op}{mod} )"
    )
    await ctx.send(
        f"{dice}d{sides}{mod_op}{mod}  ⟶  **{roll}**   ( `{inv_rolls}{mod_op}{mod}` )"
    )


bot.run(settings.discord_token)
