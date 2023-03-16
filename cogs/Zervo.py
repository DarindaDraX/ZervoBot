from time import sleep
from unicodedata import name
import discord
import asyncio
import random
import requests
from discord.ext import commands
from discord import option
from discord.commands import slash_command
import datetime

date = datetime.date.today()
year = date.year


class Zervo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="usersearch",
                            description='Get Zervo user info')
    async def _usersearch(self, ctx, username):
        response = requests.get(
            f"https://wg6.pinpon.cool/pinpon-app-system/app-user/detail/{username}",
            headers=self.bot.headers).json()
        if response['code'] != 200:
            response = requests.get(
                f"https://wg6.pinpon.cool/pinpon-app-system/v5/app-recommend/all/search?current=1&name={username}&size=3",
                headers=self.bot.headers).json()
            data = response['data']['appUserRecommendVOS']
            await ctx.respond(data)
            return
        sex = ''
        udata = response['data']
        if udata['sex'] == 0:
            sex = 'Alien'
        elif udata['sex'] == 1:
            sex = 'Male'
        elif udata['sex'] == 2:
            sex = 'Female'
        uage = udata['birthday']
        byear = int(uage[0:4])
        bday = (uage[0:10])
        age = year - byear - 1
        embed = discord.Embed(
            title=udata['nickname'],
            url=f"https://www.zervo.me/people/{udata['appUserId']}",
            description=udata['bio'],
            color=0x36383e)
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/1031232249858899988/1085202393752420482/images_19.jpg"
        )
        embed.add_field(name="Username", value=udata['id'], inline=False)
        embed.add_field(name='UserId', value=udata['appUserId'], inline=False)
        embed.add_field(name='Points', value=udata['point'], inline=False)
        embed.add_field(name='BirthDay', value=bday, inline=False)

        embed.add_field(name='Join Date',
                        value=udata['createTime'],
                        inline=False)
        embed.add_field(name='Age', value=age, inline=True)
        embed.add_field(name='Sex', value=sex, inline=True)
        embed.set_footer(text="This is development version")
        await ctx.respond(embed=embed)

    @commands.slash_command(name="register", description="register yourself")
    async def _register(self, ctx, username):
        c = self.bot
        desc = 'text'
        count = 1
        user = c.db.execute(f'select * from users where dId =?',
                            (ctx.author.id, )).fetchone()
        print(user)
        if user != None:
            await ctx.respond("You are already registered")
            return
        response = requests.get(
            f"https://wg6.pinpon.cool/pinpon-app-system/app-user/detail/{username}",
            headers=self.bot.headers).json()

        if response['code'] == 200:
            user = response['data']
            c.db.execute("insert into users values(?,?,?,?,'Null',1)",
                         (ctx.author.id, user['appUserId'], username,
                          str(ctx.author.avatar)))
            c.conn.commit()
            await ctx.respond("registered")
        else:
            await ctx.respond(f"{username} user not found")

    @commands.slash_command(name="profile", description="Get user profile")
    async def _profile(self, ctx, member: discord.Member = None):
        c = self.bot
        if member == None:
            member = ctx.author
        user = c.db.execute("select * from users where dId =?",
                            (member.id, )).fetchone()
        print(user)
        if user == None:
            await ctx.respond(f"{member.mention} not registered")
        else:
            response = requests.get(
                f"https://wg6.pinpon.cool/pinpon-app-system/app-user/detail/{user[2]}",
                headers=self.bot.headers).json()
            if response['code'] != 200:
                await ctx.respond("Something went wrong")
                return
            sex = ''
            udata = response['data']
            if udata['sex'] == 0:
                sex = 'Alien'
            elif udata['sex'] == 1:
                sex = 'Male'
            elif udata['sex'] == 2:
                sex = 'Female'
            uage = udata['birthday']
            byear = int(uage[0:4])
            bday = (uage[0:10])
            age = year - byear - 1
            embed = discord.Embed(
                title=udata['nickname'],
                url=f"https://www.zervo.me/people/{udata['appUserId']}",
                description=udata['bio'],
                color=0x36383e)
            embed.set_thumbnail(url=user[3])
            embed.add_field(name="Username", value=udata['id'], inline=False)
            embed.add_field(name='UserId',
                            value=udata['appUserId'],
                            inline=False)
            embed.add_field(name='Points', value=udata['point'], inline=False)
            embed.add_field(name='BirthDay', value=bday, inline=False)

            embed.add_field(name='Join Date',
                            value=udata['createTime'],
                            inline=False)
            embed.add_field(name='Age', value=age, inline=True)
            embed.add_field(name='Sex', value=sex, inline=True)
            embed.set_footer(
                text=
                "This is just a demo version more coming oc info, bio and discord profile and many more"
            )
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Zervo(bot))
