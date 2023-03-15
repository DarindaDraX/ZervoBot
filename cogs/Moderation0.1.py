import discord
from discord.ext import commands
from discord.commands import slash_command
guild = 1031033900547448862


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ban Command
    @commands.slash_command(name='ban', guild_ids=[guild])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = "no reason provided"
        await ctx.respond(f'User {member.mention} has been banned for "{reason}"')
        await ctx.guild.ban(member)

    # Kick Command
    @commands.slash_command(name='kick', guild_ids=[guild])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = "no reason provided"
        await ctx.respond(f'User {member.mention} has been kicked for "{reason}"')
        await ctx.guild.kick(member)


def setup(bot):
    bot.add_cog(Moderation(bot))
