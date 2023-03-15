from time import sleep
from unicodedata import name
import discord
import asyncio
import random
import requests
from discord.ext import commands
from discord import option
from discord.commands import slash_command


class Zervo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="usersearch",
                            description='Get Zervo user info')
    async def _usersearch(self, ctx, username):
        response = requests.get(
            f"https://wg6.pinpon.cool/pinpon-app-system/app-user/detail/{username}",
            headers=self.bot.headers).json()
        udata = response['data']
        message = f"""
        id :{udata['appUserId']}
        username :{udata['id']}
        nickname :{udata['nickname']}
        coiints :{udata['point']}
        """
        embed = discord.Embed(
            title=udata['nickname'],
            url=
            "https://media.discordapp.net/attachments/1031232249858899988/1085202393752420482/images_19.jpg",
            description="test",
            color=0x36383e)
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/1031232249858899988/1085202393752420482/images_19.jpg"
        )
        embed.add_field(name="username", value=udata['id'], inline=False)
        embed.set_footer(text="foot")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Zervo(bot))
