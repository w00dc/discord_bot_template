import os

import discord

# from dotenv import load_dotenv
from config import get_settings


settings = get_settings()
TOKEN = settings.discord_token


client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


client.run(TOKEN)
