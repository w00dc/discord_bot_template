import platform
import random
import re

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import random_color


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(
        name="roll", help="Simulates rolling dice given an input string"
    )
    async def roll(
        self,
        ctx: Context,
        dice_string: str = commands.parameter(
            description="Dice roll string with NO SPACES -- ie, 2d8+1 for 2 x 8-sided dice + 1"
        ),
    ) -> None:
        # Pull any Mod out of the string
        mod = 0
        mod_op = "+"
        dice_str_raw = dice_string
        if "+" in dice_string or "-" in dice_string:
            dice_and_mod = re.split("[-\+]+", dice_string)
            dice_str_raw = dice_and_mod[0]
            mod_op = re.findall("[-\+]+", dice_string)[0]
            mod = dice_and_mod[-1]
        # Split string into Num of Dice and Dice Sides
        sides_and_dice = dice_str_raw.split("d")
        # Check that the input string is valid
        if (
            len(sides_and_dice) != 2
            or any(not n.isnumeric() for n in sides_and_dice)
            or not mod.isnumeric()
        ):
            self.bot.logger.error(
                f"{dice_string} is not a valid format for the roll command"
            )
            await ctx.send(
                f"**{dice_string}** is not a valid format for the roll command"
            )
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
        self.bot.logger.info(
            f"Rolling a {dice}d{sides}{mod_op}{mod} for {ctx.author.name}  ⟶  {roll}   ( {inv_rolls}{mod_op}{mod} )"
        )
        # Create an embed to send the response in
        embed = discord.Embed(
            title="Roll Results",
            color=random_color,
        )
        embed.set_footer(f"Rolled by {ctx.author.name}")
        embed.add_field(
            name=f"{dice_string}",
            value=f"`{roll}` == `{inv_rolls}{mod_op}{mod}`",
            inline=False,
        )

        await ctx.send(
            # f"{dice}d{sides}{mod_op}{mod}  ⟶  **{roll}**   ( `{inv_rolls}{mod_op}{mod}` )",
            embed=embed,
            silent=True,
        )


async def setup(bot):
    await bot.add_cog(General(bot))
