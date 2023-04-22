import discord
from discord.ext import commands
import requests
import aiohttp
import json
import random
import datetime
import openai
import os
import re
from bs4 import BeautifulSoup

with open("db.json", "r") as json_file:
    loaded_db = json.load(json_file)

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


# Dictionary to store chat history for each user
chat_history = {}


async def chat1(ctx, prompt):

    await ctx.respond(content='*⏳ Loading...*')

    openai.api_key = os.getenv('apikey')

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content='❌ **ERROR: Your prompt is inappropriate.**')
        return

    # Retrieve username from context
    user = str(ctx.author.name)

    # Get chat history for the user, if available
    if user in chat_history:
        messages = chat_history[user]
    else:
        messages = [{
            "role":
            "system",
            "content":
            "You are a rude,cool,cute,and funny female bot, named Mikasha that serves the Zervo Discord server. You are made by DracX , DracX is bot developer and funny cute intelligent guy his instagram link and extract username from it  https://www.instagram.com/cre3pyw0rld, You reply everything in cool manner using cool words like dude ,wassup and other chat texts"
        }]

    # Append user's prompt to messages
    messages.append({'role': 'user', 'content': prompt})

    stream = []
    try:
        for r in openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                              messages=messages,
                                              user=user,
                                              stream=True):
            try:
                stream.append(r.choices[0].delta.content)
                result = "".join(stream).strip()
                await ctx.edit(content=f'{result}')

                # Update chat history with current messages
                chat_history[user] = messages + r.choices[0].message
            except:
                pass
    except:
        await ctx.edit(
            content=
            '❌ **ERROR: Mikasha is currently overloaded. Please try again.**')
        return


async def chat(ctx, prompt, user_name=None, chat_history=[]):

    await ctx.respond(content='*⏳ Loading...*')

    openai.api_key = os.getenv('apikey')

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content='❌ **ERROR: Your prompt is inappropriate.**')
        return

    if user_name is None:
        user_name = str(ctx.author.name)

    if not chat_history:
        chat_history.append({
            'role':
            'system',
            'content':
            "You are a rude, cool, sarcastic, and funny bot, named Mikasha that serves the Zervo Discord server. You are made by DracX, who is a bot developer and a funny, cute, intelligent guy. His Instagram link and extracted username from it: https://www.instagram.com/cre3pyw0rld"
        })

    chat_history.append({'role': 'user', 'content': prompt})

    stream = []
    print(chat_history)
    try:
        for r in openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                              messages=chat_history,
                                              user=user_name,
                                              stream=True):
            try:
                stream.append(r.choices[0].delta.content)
                result = "".join(stream).strip()
                await ctx.edit(content=f'{result}')
            except:
                pass
    except:
        await ctx.edit(
            content=
            '❌ **ERROR: Mikasha is currently overloaded. Please try again.**')
        return


class Zay(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chat", description="Chat with Mikasha.")
    async def _chat(self, ctx, *, prompt):
        user_name = None
        msg = await ctx.send(content='*⏳ Loading...*')

        openai.api_key = os.getenv('apikey')

        moderation = openai.Moderation.create(input=prompt)

        if moderation.results[0].flagged:
            await msg.edit(content='❌ **ERROR: Your prompt is inappropriate.**'
                           )
            return

        if user_name is None:
            user_name = str(ctx.author.name)
            chat_history[ctx.author.id] = []
        if user_name == "DracX":
            if not chat_history[ctx.author.id]:
                chat_history[ctx.author.id].append({
                    'role':
                    'system',
                    'content':
                    f"You are girlfriend of {ctx.author.name} and your name is Mikasa, you are sarcastic funny and know how to make him happy, you reply in short sentence and you are currenty talking in discord Zervo server do not let anyone know that you are bot behave like human and do not say sorry"
                })
        else:
            if not chat_history[ctx.author.id]:
                chat_history[ctx.author.id].append({
                    'role':
                    'system',
                    'content':
                    f"You are talking with {ctx.author.name} and your name is Mikasa, You are a sarcastic trolling human and you are talking in discord server"
                })

        chat_history[ctx.author.id].append({'role': 'user', 'content': prompt})
        stream = []
        try:
            for r in openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=chat_history[ctx.author.id],
                    user=user_name,
                    stream=True):
                try:
                    stream.append(r.choices[0]['delta']['content'])
                    result = "".join(stream).strip()
                    await msg.edit(content=f'{result}')
                except:
                    pass
        except:
            await ctx.edit(
                content=
                '❌ **ERROR: Mikasha is currently overloaded. Please try again.**'
            )
            return

    @commands.command(name="globalchat")
    async def _globalchat(self, ctx, channel: discord.TextChannel = None):
        if channel:
            self.bot.db.execute(
                "insert or replace into globalchat values (?,?,?,?)",
                (ctx.author.id, ctx.guild.id, channel.id, channel.name))
            self.bot.conn.commit()
            loaded_db["channels"].append(channel.id)
            await ctx.send(
                f"Successfully set **Globalchat** channel to {channel.mention}"
            )
        else:
            self.bot.db.execute("delete from globalchat where gId = ?",
                                (ctx.guild.id, ))
            self.bot.conn.commit()
            loaded_db["channels"].remove(channel.id)
            await ctx.send("Successfully removed from **Globalchat**")
        with open("db.json", "w") as json_file:
            json.dump(loaded_db, json_file)

    @commands.Cog.listener()
    async def on_message(self, message):
        channels = loaded_db["channels"]
        if message.author.bot:
            return
        if message.channel.id in channels:
            for channel_id in channels:
                for guild in self.bot.guilds:
                    target_channel = discord.utils.get(guild.text_channels,
                                                       id=channel_id)
                    if target_channel:
                        if target_channel.id != message.channel.id:
                            msg = ''
                            desc = message.content
                            user = await self.bot.fetch_user(message.author.id)
                            banner_clr = user.accent_color

                            if desc.startswith("https://tenor"):
                                response = requests.get(desc)
                                html_content = response.text
                                soup = BeautifulSoup(html_content, 'lxml')
                                img = soup.find('meta',
                                                property='og:image')['content']
                                title = soup.find(
                                    'meta', property='og:title')['content']
                                embed = discord.Embed(description=title,
                                                      color=banner_clr)
                                embed.set_image(url=f"{img}")
                            else:
                                pattern = re.compile(r'(https?://\S+)',
                                                     re.IGNORECASE)
                                matches = pattern.findall(desc)

                                for link in matches:
                                    desc = desc.replace(
                                        f"{link}", f"[link]({link})")
                                embed = discord.Embed(description=f"{desc}",
                                                      color=banner_clr)
                                if message.attachments:
                                    img = message.attachments[0]
                                elif matches:
                                    if matches[0].endswith(
                                            "png") or matches[0].endswith(
                                                "jpeg") or matches[0].endswith(
                                                    "jpg"
                                                ) or matches[0].endswith(
                                                    "gif") or matches[
                                                        0].endswith("webp"):
                                        img = matches[0]
                                        embed.set_image(url=img)

                            embed.set_author(name=message.author,
                                             icon_url=message.author.avatar)
                            if message.reference:
                                m_obj = await message.channel.fetch_message(
                                    message.reference.message_id)
                                try:
                                    emb = m_obj.embeds[0]
                                    embed.set_footer(
                                        text=
                                        f"Replied to {emb.author.name}: {emb.description[:15]}|{m_obj.guild.name}",
                                        icon_url=f"{emb.author.icon_url}")
                                except:
                                    embed.set_footer(
                                        text=
                                        f"Replied to {m_obj.author.name}: {m_obj.content[:15]} | {m_obj.guild.name}",
                                        icon_url=f"{m_obj.author.avatar}")
                            else:
                                embed.set_footer(
                                    text=f"{message.guild.name}",
                                    icon_url=f"{message.guild.icon}")
                            embed.timestamp = datetime.datetime.utcnow()
                            await target_channel.send(embed=embed)
                            await message.add_reaction("✅")
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
                        duser = self.bot.get_user(dec)
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
                                "kiss", "hug", "cuddle", "nuzzle", "pat",
                                "smack", "handhold"
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
                        if message.author.name == "DracXxxx":
                            for x in range(10):
                                await message.reply(embed=embed)
                        await message.reply(embed=embed)
        if message.channel.id == 1085978090011902084:
            if message.author.id != self.bot.user.id:
                content = message.content
                await message.reply(
                    chatbot(message, content)['choices'][0]['text'])
        elif message.content.lower().startswith('miko'):
            content = message.content[3:]
            await message.reply(
                chatbot(message, content)['choices'][0]['text'])


def setup(bot):
    bot.add_cog(Zay(bot))
