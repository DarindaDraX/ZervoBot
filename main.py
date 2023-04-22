import discord
from discord.ext import commands
import sqlite3

import os
import random
import subprocess
import shlex
import asyncio
import datetime
import requests
import aiohttp
import openai
import keep_alive

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

db.execute("""
    create table IF NOT EXISTS globalchat(
    dId INT NOT NULL,
    gId INT NOT NULL,
    cId INT NOT NULL,
    cName TEXT 
    )
    """)
conn.commit()

colors = {
    'DEFAULT': 0x000000,
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'GREY': 0x95A5A6,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_GREY': 0x979C9F,
    'DARKER_GREY': 0x7F8C8D,
    'LIGHT_GREY': 0xBCC0C0,
    'DARK_NAVY': 0x2C3E50,
    'BLURPLE': 0x7289DA,
    'GREYPLE': 0x99AAB5,
    'DARK_BUT_NOT_BLACK': 0x2C2F33,
    'NOT_QUITE_BLACK': 0x23272A
}


class MyHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        if isinstance(mapping, set):
            mapping = {cog: cog.get_commands() for cog in mapping}
        channel = self.get_destination()
        help_embed = discord.Embed(
            title='Help',
            description="Use command\n**zay** help\n**/help**",
            color=colors['DARK_BUT_NOT_BLACK'])
        help_embed.set_thumbnail(url=bot.user.avatar.url)
        await channel.send(embed=help_embed)


bot = commands.Bot(command_prefix='?',
                   intents=discord.Intents.all(),
                   help_command=MyHelp(),
                   activity=discord.Activity(
                       type=discord.ActivityType.listening, name='?help'))
cogs = [
    'cogs.Interaction', 'cogs.Fun', 'cogs.Zervo', 'cogs.Custom', 'cogs.Zay'
]
for cog in cogs:
    bot.load_extension(cog)


@bot.event
async def on_ready():
    print("About the bot:")
    print(f"Username: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    bot.conn = conn
    bot.db = db
    for guild in bot.guilds:
        print(guild)


@bot.event
async def on_member_join(member):
    await member.send("Welcome to the server")


@bot.command(name="addrole")
async def add_role(ctx, member: discord.Member):
    guild = discord.utils.get(bot.guilds, name="Rizzland")
    target_guild = await bot.fetch_guild(guild.id)
    if target_guild:
        role = discord.utils.get(target_guild.roles, id=1085602292981575690)
        print(role.id)
        if role:
            await member.add_roles(role)
            await ctx.send("Role added successfully!")
        else:
            await ctx.send("Role not found in the guild.")
    else:
        await ctx.send("Guild not found.")


@bot.command(name="checkpermissions")
async def check_permissions(ctx):
    # Get the bot's role in the target guild
    guild = discord.utils.get(bot.guilds, name="Rizzland")
    if guild:
        bot_role = guild.get_member(
            bot.user.id).roles[-1]  # Assumes the bot has only one role
        permissions = bot_role.permissions

        # Check specific permissions
        if permissions.manage_roles:
            await ctx.send("Bot has 'Manage Roles' permission.")
        else:
            await ctx.send("Bot does not have 'Manage Roles' permission.")
    else:
        await ctx.send("Guild not found.")


@bot.slash_command(name="sendmessage")
async def send_message(ctx, guild_name: str, channel_name: str, message: str):
    # Find the target guild by name
    target_guild = discord.utils.get(bot.guilds, name=guild_name)
    if target_guild:
        # Find the target channel in the target guild by name
        target_channel = discord.utils.get(target_guild.text_channels,
                                           name=channel_name)
        if target_channel:
            # Send the message in the target channel
            await target_channel.send(message)
            await ctx.respond("Message sent successfully!")
        else:
            await ctx.respond(
                f"Channel '{channel_name}' not found in the guild '{guild_name}'."
            )
    else:
        await ctx.respond(f"Guild '{guild_name}' not found.")


@bot.command(name="a")
async def a(ctx, member: discord.Member, role: discord.Role):
    await ctx.message.delete()
    print(role)
    print(type(role))
    await member.add_roles(role)


@bot.command()
async def py(ctx, *, command: str):
    if ctx.author.id != 632748789341618207:
        await ctx.send("only drax can use this")
        return
    try:
        output = subprocess.check_output(['python3', '-c', f'{command}'],
                                         stderr=subprocess.STDOUT,
                                         text=True)
        #output = subprocess.check_output(command + ' 2>&1', shell=True, text=True)
        embed = discord.Embed(description=output,
                              color=colors['DARK_BUT_NOT_BLACK'])
        await ctx.send(embed=embed)
    except subprocess.CalledProcessError as e:
        embed = discord.Embed(title="ERROR",
                              description=f"{e.returncode}\n{e.output}")
        await ctx.send(embed=embed)
    except Exception as ex:
        await ctx.send(f'Error: {ex}')


@bot.command()
async def bash(ctx, *, command: str):
    if ctx.author.id != 632748789341618207:
        await ctx.send("only drax can use this")
        return
    try:
        #output = subprocess.check_output(['python3', '-c', f'{command}'],stderr=subprocess.STDOUT,text=True)
        output = subprocess.check_output(command + ' 2>&1',
                                         shell=True,
                                         text=True)
        embed = discord.Embed(description=output,
                              color=colors['DARK_BUT_NOT_BLACK'])
        await ctx.send(embed=embed)
    except subprocess.CalledProcessError as e:
        embed = discord.Embed(title="ERROR",
                              description=f"{e.returncode}\n{e.output}")
        await ctx.send(embed=embed)
    except Exception as ex:
        await ctx.send(f'Error: {ex}')


@bot.command()
async def sh(ctx, *, command: str):
    if ctx.author.id != 632748789341618207:
        await ctx.send("only drax can use this")
        return
    try:
        args = shlex.split(command)
        if args[0] == 'cd':
            os.chdir(args[1])
            output = f"Changed directory to: {args[1]}"
            embed = discord.Embed(description=output)
            await ctx.send(embed=embed)

        else:
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            stdout = stdout.decode()
            stderr = stderr.decode()
            embed = discord.Embed(description=f"**Output**:\n{stdout}",
                                  color=colors['DARK_BUT_NOT_BLACK'])
            embed.set_footer(text=stderr)
            await ctx.send(embed=embed)

    except Exception as ex:
        await ctx.send(f'Error: {ex}')


@bot.command()
async def sql(ctx, *, command: str):
    if ctx.author.id != 632748789341618207:
        await ctx.send("Only authorized users can use this command.")
        return
    try:
        db.execute(command)
        result = db.fetchall()
        conn.commit()
        embed = discord.Embed(description=result,
                              color=colors['DARK_BUT_NOT_BLACK'])
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error: {e}")


keep_alive.keep_alive()

try:
    bot.run(os.environ.get('TOKEN'))
except:
    os.system('kill 1')
