import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Greetings(commands.Cog, name="greetings"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome {member.mention}.")

    @commands.hybrid_command(name="greet", help="Get an emoji greeting!")
    async def greeting(self, ctx: Context) -> None:
        emojis = [
            ":poop:",
            ":wave:",
            ":+1:",
        ]

        response = random.choice(emojis)
        self.bot.logger.info(f"Responding to {ctx.author.name} with a {response}")
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(Greetings(bot))
