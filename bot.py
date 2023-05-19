import os

import discord

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

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


client.run(TOKEN)
