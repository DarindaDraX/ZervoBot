from time import sleep
from unicodedata import name
import discord
import asyncio
import random
import requests
from discord.ext import commands
from discord import option
from discord.commands import slash_command

guild = 1031033900547448862


class Fun(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# 8Ball - Returns a random answer

	@commands.slash_command(name="hack", guild_ids=[guild])
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

	@commands.slash_command(name='waifu', guild_ids=[guild])
	@option("catagory",
	        description="Choose chatagory",
	        choices=["cuddle", "neko", "shinobu", 'megumin', 'bully', 'waifu'])
	async def _waifu(self, ctx: discord.ApplicationContext, catagory=None):
		if catagory == None:
			catagory = 'waifu'
		res = requests.get(f'https://api.waifu.pics/sfw/{catagory}')
		url = res.json()
		await ctx.respond(url['url'])

	@commands.slash_command(name='custommeme', guild_ids=[guild])
	async def _custommeme(self, ctx, keyword=None):
    if keyword == None:
        res = requests.get('https://meme-api.herokuapp.com/gimme').json()
        title,url = res['title'],res['url']
        await ctx.respond(f'{title} \n{url}')
    else:
        res = requests.get(f'https://api.memegen.link/images/custom?filter={keyword}&safe=false')
        meme = res.json()
        x = meme[0]['url']
        await ctx.respond(x)
		


def setup(bot):
	bot.add_cog(Fun(bot))
