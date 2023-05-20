import asyncio
import json
import os
import logging
import platform
import discord
import random
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

# from dotenv import load_dotenv
from config import get_settings


settings = get_settings()
TOKEN = settings.discord_token


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

bot = Bot(
    command_prefix=commands.when_mentioned_or(settings.cmd_prefix),
    intents=intents,
    help_command=None,
)

# Setup the loggers


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
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
    bot.logger.info(f"")
    await ctx.send(response)


@bot.command(name="roll", help="Simulates rolling dice returning the total")
async def roll(ctx, dice_str: str):
    sides_and_dice = dice_str.split("d")
    if len(sides_and_dice) != 2:
        bot.logger.error(f"{dice_str} is not a valid format for the roll command")
        return
    number_of_sides = int(sides_and_dice[1])
    number_of_dice = int(sides_and_dice[0])
    roll = 0
    for i in range(number_of_dice):
        roll += random.choice(range(1, number_of_sides + 1))
    await ctx.send(roll)


bot.run(TOKEN)
