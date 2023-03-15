""""
Ignite Discord Bot
Original by VanDerFire
MIT License
(C)2021-2022
"""
import discord
import os
from discord.ext import commands
import keep_alive
import requests
import json
# Open config.json

response = {}
headers = {}
zervobot = ""


def login():
    global response
    global headers
    header = {
        "User-Agent": "Dart/2.18 (dart:io)",
        "language": "en_IN",
        "content-type": "application/x-www-form-urlencoded;charset=utf-8",
        # "content-type":"application/json; charset=utf-8",
        "app": "zervo",
        "host": "wg6.pinpon.cool",
        "platform": "0"
    }
    data = {
        "email": "rushhours900@gmail.com",
        "password": "noxtox@69",
    }
    header['content-type'] = "application/x-www-form-urlencoded;charset=utf-8"
    response = requests.post(
        "https://wg6.pinpon.cool/pinpon-app-auth/v3/auth/login/email",
        data=data,
        headers=header).json()

    token = response["data"]["pinponToken"]["token"]
    if response['code'] == 200:
        header["pinpon-auth"] = token
        headers = header
        user_id = response['data']['appUserId']
        user_name = response['data']['id']
        print(f"logged in as {user_id}: {user_name}")
        bot.zervobot = user_name


# Bot Configuration
bot = commands.Bot(command_prefix='?',
                   activity=discord.Activity(
                       type=discord.ActivityType.listening,
                       name='master DraX!'),
                   intents=discord.Intents.all())

# Bot Events
#activity=discord.Game(name='with your daddy')
cogs = ['cogs.Interaction', 'cogs.Moderation', 'cogs.Fun', 'cogs.Zervo']


@bot.event
async def on_ready():
    print("About the bot:")
    print(f"Username: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    login()
    bot.headers = headers
    bot.response = response
    bot.remove_command('help')


# Bot Commands

# Example command

guild = 1033800504121241630
# Put here the IDs of the servers where you want the bot to run, this can be omitted, but keep in mind that new commands may take up to an hour to be registered (This applies to all slash-type commands, including cogs)

#@bot.slash_command(guild_ids=[guild])
#async def say(ctx, message):
#    await ctx.respond(message)

for cog in cogs:
    bot.load_extension(cog)
keep_alive.keep_alive()
# Run the bot
try:
    bot.run(os.environ.get('TOKEN'))
except:
    os.system('kill 1')
