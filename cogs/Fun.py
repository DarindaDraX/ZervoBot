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
from replit import db

guild = 1031033900547448862

link = ["error"]
count = 0


def save(links):
    with open("response.py", "w") as f:
        f.write(links)


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # 8Ball - Returns a random answer

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
    async def _nsfwwaifu(self, ctx: discord.ApplicationContext, catagory=None):
        if catagory == None:
            catagory = 'waifu'
        res = requests.get(f'https://api.waifu.pics/nsfw/{catagory}')
        url = res.json()
        await ctx.respond(url['url'], delete_after=1000)

    @commands.slash_command(name='meme', description='Meme and meme and meme')
    async def _meme(self, ctx, keyword=None):
        if keyword == None:
            res = requests.get('https://meme-api.herokuapp.com/gimme').json()
            title, url = res['title'], res['url']
            await ctx.respond(f'{title} \n{url}')
        else:
            await ctx.response.defer()
            res = requests.get(
                f'https://api.memegen.link/images/custom?filter={keyword}&safe=false'
            ).json()
            l = random.choice(res)
            await ctx.followup.send(l['url'])

    @commands.slash_command(name="search", description='Search image')
    async def _search(self, ctx, query):
        global link
        global count
        links = []
        count = 0
        link = []
        url = f"https://www.bing.com/images/search?q={query}"
        #url = f"https://www.bing.com/images/search?q=&safesearch=off"
        custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

        res = requests.get(url, headers={
            "User-Agent": custom_user_agent,
        })
        soup = BeautifulSoup(res.content, 'lxml')
        for a in soup.find_all("a", {"class": "iusc"}):
            m = json.loads(a["m"])
            murl = m["murl"]
            links.append(murl)

        link = links
        if links:
            await ctx.respond(links[0])
        else:
            await ctx.respond(f"[{query} ] may contain banned words")

    @commands.slash_command(name="image", description='Search image')
    async def _image(self, ctx, query):
        url = f"https://yandex.com/images/search?text={query}"
        custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        print(url)
        res = requests.get(url, headers={
            "User-Agent": custom_user_agent,
        })
        soup = BeautifulSoup(res.content, 'lxml')
        links = []
        for a in soup.find_all("div", {"class": "serp-item"}):
            m = json.loads(a["data-bem"])
            imgs = m['serp-item']['preview']
            img = imgs[0]
            url = img['url']
            links.append(url)
        if links:
            await ctx.respond(links[0])
        else:
            await ctx.respond("Your search contains banned words ")

    @commands.Cog.listener()
    async def on_message(self, message):
        global link
        global count
        if message.content.lower() == "next":
            count = 1 + count
            messagex = str(link[count])
            print(count)
            await message.reply(messagex)
        elif message.content.lower() == "prev":
            count = count - 1
            print(count)
            messagesy = str(link[count])
            await message.reply(messagesy)

    @commands.slash_command(name="say", description='say somethingg')
    async def _say(self, ctx, message):
        await ctx.respond(message)


def setup(bot):
    bot.add_cog(Fun(bot))
