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
import sqlite3
import openai
import aiohttp
import datetime
import random

response = {}
headers = {}
zervobot = ""

conn = sqlite3.connect("zervo.db")

db = conn.cursor()

db.execute("""
    create table IF NOT EXISTS users(
    dId INT PRIMARY KEY,
    zid INT NOT NULL,
    username TEXT NOT NULL,
    pUrl TEXT,
    desc TEXT,
    mCount INT
    )
    """)
conn.commit()

bot = commands.Bot(command_prefix='?',
                   activity=discord.Activity(
                       type=discord.ActivityType.listening,
                       name='master DraX!'),
                   intents=discord.Intents.all())

# Bot Events
#activity=discord.Game(name='with your daddy')
cogs = ['cogs.Interaction', 'cogs.Fun', 'cogs.Zervo']


@bot.event
async def on_ready():
    print("About the bot:")
    print(f"Username: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")

    bot.conn = conn
    bot.db = db
    bot.remove_command('help')


@bot.event
async def on_member_join(member):
    await member.send("Welcome to the server")


def chatbot(message, content):
    openai.api_key = os.environ.get('apikey')
    username = str(message.author)
    name = str(username[:-5])
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=f"{name}:{content}",
                                        temperature=0.9,
                                        max_tokens=100,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0.6,
                                        stop=[" zervobot:", " user:"])
    print(name)
    return response


keyword = [
    'baka', 'bite', 'blush', 'bored', 'cry', 'cuddle', 'dance', 'facepalm',
    'feed', 'handhold', 'happy', 'highfive', 'hug', 'kick', 'kiss', 'laugh',
    'nod', 'nom', 'nope', 'pat', 'poke', 'pout', 'punch', 'shoot', 'shrug',
    'slap', 'sleep', 'smile', 'smug', 'stare', 'think', 'thumbsup', 'tickle',
    'wave', 'wink', 'yeet'
]
continuous_forms = {
    'baka': 'baka-ing',
    'bite': 'biting',
    'blush': 'blushing',
    'bored': 'boring',
    'cry': 'crying',
    'cuddle': 'cuddling',
    'dance': 'dancing',
    'facepalm': 'facepalming',
    'feed': 'feeding',
    'handhold': 'handholding',
    'happy': 'happying',
    'highfive': 'highfiving',
    'hug': 'hugging',
    'kick': 'kicking',
    'kiss': 'kissing',
    'laugh': 'laughing',
    'nod': 'nodding',
    'nom': 'nomming',
    'nope': 'nope-ing',
    'pat': 'patting',
    'poke': 'poking',
    'pout': 'pouting',
    'punch': 'punching',
    'shoot': 'shooting',
    'shrug': 'shrugging',
    'slap': 'slapping',
    'sleep': 'sleeping',
    'smile': 'smiling',
    'smug': 'smugging',
    'stare': 'staring',
    'think': 'thinking',
    'thumbsup': 'thumbs-upping',
    'tickle': 'tickling',
    'wave': 'waving',
    'wink': 'winking',
    'yeet': 'yeeting'
}

emojis = {
    'baka': ['🙄', '😒', '🤪'],
    'bite': ['🦷', '🍴', '😬'],
    'blush': ['🥰', '😊', '😳'],
    'bored': ['😴', '🥱', '😑'],
    'cry': ['😢', '😭', '😿'],
    'cuddle': ['🤗', '🫂', '😻'],
    'dance': ['💃', '🕺', '🎶'],
    'facepalm': ['🤦‍♀️', '🤦‍♂️', '😖'],
    'feed': ['🍽️', '🥄', '🐦'],
    'handhold': ['🤝', '👐', '💞'],
    'happy': ['😁', '😄', '😊'],
    'highfive': ['👋', '🤚', '🙌'],
    'hug': ['🤗', '🫂', '👫'],
    'kick': ['🦵', '👟', '🤜'],
    'kiss': ['😘', '💋', '👄'],
    'laugh': ['😂', '🤣', '😆'],
    'nod': ['👍', '🙌', '👌'],
    'nom': ['🍴', '🍔', '😋'],
    'nope': ['🙅‍♀️', '🙅‍♂️', '👎'],
    'pat': ['👏', '🐶', '🤗'],
    'poke': ['👉', '👈', '🙄'],
    'pout': ['😞', '😔', '😣'],
    'punch': ['🥊', '🤜', '👊'],
    'shoot': ['🔫', '💥', '🎯'],
    'shrug': ['🤷‍♀️', '🤷‍♂️', '🤔'],
    'slap': ['👋', '🤚', '👋‍♂️'],
    'sleep': ['😴', '💤', '🌙'],
    'smile': ['😃', '🙂', '😊'],
    'smug': ['😏', '😎', '🤨'],
    'stare': ['👀', '👁️', '😳'],
    'think': ['🤔', '💭', '🧐'],
    'thumbsup': ['👍', '👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿'],
    'tickle': ['🤭', '😆', '🤗'],
    'wave': ['👋', '👋🏻', '👋🏼', '👋🏽', '👋🏾', '👋🏿'],
    'wink': ['😉', '😜', '😘'],
    'yeet': ['🦵']
}


@bot.event
async def on_message(message):
    if message.content.lower().startswith("zay"):

        msg = str(message.content)[3:].lower().split()
        found_member = False
        print(msg)
        if not msg:
            return
        elif len(msg) >= 2:
            action = msg[0]
            user = msg[1]
            if user.startswith("<@"):
                dec = int(user.replace("<@", "").replace('>', ""))
                duser = bot.get_user(dec)
                user = duser.name
                pass
            else:
                for name in message.guild.members:
                    if name.name.lower().startswith(user) or \
                    (name.nick is not None and name.nick.lower().startswith(user)):
                        user = name.name
                        found_member = True
                        break
                    else:
                        continue
                    break
                if not found_member:
                    await message.reply(
                        f"No member found with name starting with {msg}")
                    return
        elif len(msg) == 1:
            user = None
            action = msg[0]
        if action in keyword:
            print(True)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://nekos.best/api/v2/{action}") as resp:
                    data = await resp.json()
                    emoji = random.choice(emojis[action])
                    if user == None:
                        embed = discord.Embed(
                            description=
                            f'{emoji} **{message.author.name}** {continuous_forms[action]}',
                            color=discord.Colour.blue())
                    else:
                        embed = discord.Embed(
                            description=
                            f'{emoji} **{message.author.name}** {continuous_forms[action]} to **{user}**',
                            color=discord.Colour.blue())
                    embed.set_image(url=data["results"][0]["url"])
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text=action)
                    await message.reply(embed=embed)
    if message.channel.id == 1085978090011902084:
        if message.author.id != bot.user.id:
            content = message.content
            await message.reply(
                chatbot(message, content)['choices'][0]['text'])
    elif message.content.lower().startswith('bot'):
        content = message.content[3:]
        await message.reply(chatbot(message, content)['choices'][0]['text'])


guild = 1033800504121241630

for cog in cogs:
    bot.load_extension(cog)
keep_alive.keep_alive()

try:
    bot.run(os.environ.get('TOKEN'))
except:
    os.system('kill 1')
