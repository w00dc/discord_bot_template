import asyncio
import json
import os
import logging
import platform
import discord
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
    The code in this event is executed when the bot is ready
    """
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")
    if settings.sync_commands_globally:
        bot.logger.info("Syncing commands globally...")
        await bot.tree.sync()


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot starts
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")


asyncio.run(load_cogs())
bot.run(settings.discord_token)
