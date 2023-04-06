from time import sleep
import discord
import asyncio
import random
import requests
from discord.ext import commands
from discord import option
from discord.commands import slash_command
from bs4 import BeautifulSoup
import json
import openai

db = {}
guild = 1031033900547448862


def save(links):
    with open("response.py", "w") as f:
        f.write(links)


class MyView(discord.ui.View):

    def __init__(self, bot, ctx, caption, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.ctx = ctx
        self.caption = caption

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="◀")
    async def button_callback2(self, button, interaction):
        global db
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                content="You are not author of this message", ephemeral=True)
            return
        db[self.ctx.author.id][1] -= 1
        count = db[self.ctx.author.id][1]
        links = db[self.ctx.author.id][0]

        embed = discord.Embed(
            description=f"{self.caption} {count}/{len(links)}",
            color=discord.Colour.blue())
        embed.set_image(url=links[count])
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="▶")
    async def button_callback(self, button, interaction):
        global db
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                content="You are not author of this message", ephemeral=True)
            return
        db[self.ctx.author.id][1] += 1
        count = db[self.ctx.author.id][1]
        links = db[self.ctx.author.id][0]

        embed = discord.Embed(
            description=f"{self.caption} {count}/{len(links)}",
            color=discord.Colour.blue())
        embed.set_image(url=links[count])
        await interaction.response.edit_message(embed=embed)


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="testing")
    async def testing(ctx, message):
        await ctx.respond(message)

    @commands.slash_command(name="hack", description='Hack someone')
    async def _hack(self, ctx, user: discord.Member):
        msg = await ctx.send(f'hacking {user.name}')
        await asyncio.sleep(3.0)
        await msg.edit(content='Finding IP address')
        await asyncio.sleep(3.0)
        await msg.edit(content='IP : 192.168.12.3')
        await asyncio.sleep(3.0)
        await msg.edit(content='Finding user email address')
        await asyncio.sleep(3.0)
        await msg.edit(content=f'user email: {user.name}@discord.com')
        await asyncio.sleep(1)
        await msg.edit(content='Hacking completed')

    @commands.slash_command(name='waifu', description='Random pics/gif')
    @option("catagory",
            description="Choose chatagory",
            choices=["cuddle", "neko", "shinobu", 'megumin', 'bully', 'waifu'])
    async def _waifu(self, ctx: discord.ApplicationContext, catagory=None):
        if catagory == None:
            catagory = 'waifu'
        res = requests.get(f'https://api.waifu.pics/sfw/{catagory}')
        url = res.json()
        await ctx.respond(url['url'])

    @commands.slash_command(name='nsfwwaifu',
                            description='Random nsfw pics/gif')
    @option("catagory",
            description="Choose chatagory",
            choices=["waifu", "neko", 'trap', 'blowjob'])
    @commands.is_nsfw()
    async def _nsfwwaifu(self, ctx: discord.ApplicationContext, catagory=None):
        if catagory == None:
            catagory = 'waifu'
        res = requests.get(f'https://api.waifu.pics/nsfw/{catagory}')
        url = res.json()
        await ctx.respond(url['url'], delete_after=1000)

    @_nsfwwaifu.error
    async def _nsfwwaifu_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.respond(
                f"{ctx.author.mention} Use it on nsfw channel hornyass")

    @commands.slash_command(
        name="image",
        description=
        'Search image specifiy wallpaper/gif/png/jpg to get similar images')
    async def _image(self, ctx, query, caption: str = None):
        global db
        links = []
        url = f"https://www.bing.com/images/search?q={query}&safesearch=off"
        custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

        res = requests.get(url, headers={
            "User-Agent": custom_user_agent,
        })
        soup = BeautifulSoup(res.content, 'lxml')
        for a in soup.find_all("a", {"class": "iusc"}):
            m = json.loads(a["m"])
            murl = m["murl"]
            links.append(murl)
        if caption == None:
            view = MyView(self.bot, ctx, caption=" ")
        else:
            view = MyView(self.bot, ctx, caption)
        if links:
            db[ctx.author.id] = [links, 0]
            embed = discord.Embed(description=caption,
                                  color=discord.Colour.blue())
            embed.set_image(url=links[0])
            await ctx.respond(embed=embed, view=view)
        else:
            await ctx.respond(f"[{query} ] may contain banned words")

    @commands.slash_command(name='spam')
    async def _spam(self, ctx, message: str, count: int):
        for x in range(1, count):
            await ctx.respond(message)


def setup(bot):
    bot.add_cog(Fun(bot))
