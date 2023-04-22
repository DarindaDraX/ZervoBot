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

db.execute("""
    create table IF NOT EXISTS reactions(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    dId INT NOT NULL,
    keyword TEXT,
    desc TEXT,
    link TEXT,
    if_mention TEXT,
    if_None TEXT
    )
    """)
conn.commit()

# Bot Configuration
bot = commands.Bot(command_prefix='?',
                   activity=discord.Activity(
                       type=discord.ActivityType.listening,
                       name='master DraX!'),
                   intents=discord.Intents.all())

# Bot Events
#activity=discord.Game(name='with your daddy')
cogs = ['cogs.Interaction', 'cogs.Fun', 'cogs.Zervo', 'cogs.Custom']


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


key_to = [
    'baka', 'bite', 'blush', 'cuddle', 'facepalm', 'feed', 'highfive', 'hug',
    'kick', 'kiss', 'nod', 'nom', 'nope', 'pat', 'poke', 'pout', 'punch',
    'shoot', 'shrug', 'slap', 'smile', 'smug', 'stare', 'thumbsup', 'tickle',
    'wave', 'wink', 'yeet'
]
key_with = [
    'bored', 'cry', 'dance', 'handhold', 'happy', 'laugh', 'sleep', 'think'
]

keys = [
    "airkiss", "angrystare", "bite", "bleh", "blush", "brofist", "celebrate",
    "cheers", "clap", "confused", "cool", "cry", "cuddle", "dance", "drool",
    "evillaugh", "facepalm", "handhold", "happy", "headbang", "hug", "kiss",
    "laugh", "lick", "love", "mad", "nervous", "no", "nom", "nosebleed",
    "nuzzle", "nyah", "pat", "peek", "pinch", "poke", "pout", "punch", "roll",
    "run", "sad", "scared", "shrug", "shy", "sigh", "sip", "slap", "sleep",
    "slowclap", "smack", "smile", "smug", "sneeze", "sorry", "stare", "stop",
    "surprised", "sweat", "thumbsup", "tickle", "tired", "wave", "wink",
    "woah", "yawn", "yay", "yes"
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

keywords = []
keywords.extend(key_to)
keywords.extend(key_with)


@bot.event
async def on_message(message):
    if message.content.lower().startswith("zay"):
        msg = str(message.content)[3:].lower().split()
        found_member = False
        if not msg:
            return
        cmd = msg[0]
        if cmd in keys:
            if len(msg) >= 2:
                action = msg[0]
                user = msg[1]
                if user.startswith("<@"):
                    dec = int(user.replace("<@", "").replace('>', ""))
                    duser = bot.get_user(dec)
                    user = duser.name
                    pass
                elif user == 'random':
                    user = random.choice(
                        [name.name for name in message.guild.members])
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
                            f"No member found with name starting with {msg[1]}"
                        )
                        return
            elif len(msg) == 1:
                user = None
                action = msg[0]
            #"https://nekos.best/api/v2/{action}"
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"https://api.otakugifs.xyz/gif?reaction={action}"
                ) as resp:
                    data = await resp.json()
                    emoji = ' '  #random.choice(emojis[action])
                    if action in [
                            "kiss", "hug", "cuddle", "nuzzle", "pat", "smack",
                            "handhold"
                    ]:
                        action_ = action + 'ed'
                        to_or_with = 'to'
                    elif action in ["bite", "pinch", "poke", "punch"]:
                        action_ = action + 'ed'
                        to_or_with = 'on'
                    elif action in ["wave", "headbang", "nod", "shake"]:
                        action_ = action + 'ed'
                        to_or_with = 'at'
                    elif action in ["sleep", "snore"]:
                        action_ = action + 'ing'
                        to_or_with = 'with'
                    elif action in [
                            "sad",
                    ]:
                        to_or_with = 'with'
                        action_ = "is sad"
                    else:
                        action_ = action + 'ing'
                        to_or_with = 'to'
                    if user == None:
                        embed = discord.Embed(
                            description=
                            f'{emoji} **{message.author.name}** {action_}',
                            color=discord.Colour.blue())
                    else:
                        embed = discord.Embed(
                            description=
                            f'{emoji} **{message.author.name}** {action_} {to_or_with} **{user}**',
                            color=discord.Colour.blue())
                    embed.set_image(url=data["url"])
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
