import discord
import datetime
import time
import json
import os
import uuid
import shortuuid
from discord.ext import tasks, commands
from discord.ext.commands.context import Context
from cogs.utils.embeds import ErrorEmbed, PermissionDeniedEmbed
from cogs.utils.errors import send_error_embed


class MerxEvents(commands.Cog):
    def __init__(self, merx):
        self.merx = merx

    @commands.Cog.listener()
    async def on_ready(self, ctx: commands.Context = None):
        await self.merx.change_presence(activity=discord.Activity(name="mb-help | beta.merxbot.xyz", type=discord.ActivityType.watching))
        print(self.merx.user.name + " is ready.")
            
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
        if welcome_channel:
            member_count = member.guild.member_count
            await welcome_channel.send(f"> {member.mention} Welcome to **{member.guild.name}**! Feel free to explore. We now have **{member_count}** members. 🎉")            


    # This handles the permission denied and error embeds. It also generates
    # the UUID for the error embed.

    async def handle_permission_denied(self, ctx):
        embed = PermissionDeniedEmbed()
        await ctx.send(embed=embed)


    async def handle_error(self, ctx, error):
        if hasattr(ctx, 'handled'):
            return
        error_id = shortuuid.ShortUUID().random(length=8)
        if isinstance(ctx, discord.Interaction):
            await send_error_embed(ctx, error, error_id)
        else:
            await ctx.send(embed=ErrorEmbed(error=error, error_id=error_id))


    # These are the cog error handlers they determine how the error is sent.

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.handle_error(ctx, error.original if isinstance(error, commands.CommandInvokeError) else error)


    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        await self.handle_error(interaction, error)


async def setup(merx):
  await merx.add_cog(MerxEvents(merx))