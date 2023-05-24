import platform
import random
import request

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Steam(commands.Cog, name="steam"):
    def __init__(self, bot):
        self.bot = bot

    # GET https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1
    @commands.hybrid_command(
        name="player_count",
        help="Get the current player count of the specified Steam App",
    )
    async def player_count(
        self,
        ctx: Context,
        app_id: str = commands.parameter(description="Steam App ID"),
    ) -> None:
        # TODO: Implement GET call
        await ctx.send("TODO: Implement")


async def setup(bot):
    await bot.add_cog(Steam(bot))
