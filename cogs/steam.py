import platform
import random
import requests

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from config import get_settings

settings = get_settings()


class Steam(commands.Cog, name="steam"):
    def __init__(self, bot):
        self.bot = bot

    # Get all Steam Apps
    # GET https://api.steampowered.com/ISteamApps/GetAppList/v2

    # Get news for Steam App
    # GET https://api.steampowered.com/ISteamNews/GetNewsForApp/v2

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
        self.bot.logger.info(
            f"player_count called by {ctx.author.name} with app_id {app_id}"
        )
        response = requests.get(
            settings.steam_url
            + "ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
            + f"?appid={app_id}",
            headers={"x-webapi-key": settings.steam_webapi_token},
            timeout=15,
        ).json()
        self.bot.logger.info(f"Response == {response}")
        # response['response']['player_count'] is the number of players
        num_players = response["response"]["player_count"]
        await ctx.send(
            content=f"Number of people playing Steam App {app_id} is **{num_players}**",
            # silent=True,
        )

    # GET https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/
    @commands.hybrid_command(
        name="achievement_stats",
        help="Get the achievement percentages for the specified Steam App",
    )
    async def achievement_stats(
        self,
        ctx: Context,
        app_id: str = commands.parameter(description="Steam App ID"),
    ) -> None:
        self.bot.logger.info(
            f"achievement_stats called by {ctx.author.name} with app_id {app_id}"
        )
        response = requests.get(
            settings.steam_url
            + "ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/"
            + f"?gameid={app_id}",
            headers={"x-webapi-key": settings.steam_webapi_token},
            timeout=15,
        ).json()
        self.bot.logger.info(f"Response == {response}")

        await ctx.send(
            content=f"Game {app_id} has {len(response['achievementpercentages']['achievements'])} Achievements",
            # silent=True,
        )


async def setup(bot):
    await bot.add_cog(Steam(bot))
