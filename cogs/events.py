import discord
import datetime
import time
import json
import os
import uuid
import shortuuid
from discord import Embed
from discord.ext import tasks, commands
from discord.ext.commands.context import Context
from cogs.utils.embeds import ErrorEmbed, PermissionDeniedEmbed
from cogs.utils.errors import send_error_embed
from cogs.utils.constants import MerxConstants



CHANNEL_NAME_FOR_WELCOME = ["chat", "general"]
constants = MerxConstants()
prefix =  constants.prefix_setup


class MerxEvents(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.change_status.start()
        self.beta_guilds = [
            1285107028892717118, # Merx Systems Discord
        ]
        
        
    
    # This starts the activity and gets the users and guilds and sets it initally.
    
    @commands.Cog.listener()
    async def on_ready(self):
        guild_count = len(self.merx.guilds)
        user_count = sum(guild.member_count for guild in self.merx.guilds)

        await self.merx.change_presence(activity=discord.Activity(
            name=f"{guild_count} Guilds • {user_count:,} Users • /help",
            type=discord.ActivityType.watching
        ))

        print(f"{self.merx.user.name} is ready with {guild_count} guilds and {user_count:,} users.")
        
        
        
    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context):
        if ctx.author == self.merx.user:
            return
        
        try:
            if self.merx.user.mentioned_in(ctx) and len(ctx.content.split(' ')) == 1 and ctx.content[-1] == ">" and ctx.content[0] == '<':
                return await ctx.channel.send(f"My prefix is `{prefix}`, try to use `{prefix}help` for a list of commands!")
        except:
            pass
    


    if constants.merx_environment_type() == "Development":
        @commands.Cog.listener()
        async def on_ready(self):
            for guild in self.merx.guilds:
                id = guild.id
                owner = guild.get_member(guild.owner_id)
                is_dev_guild = id in self.beta_guilds
                channel = self.merx.get_guild(self.beta_guilds[0]).get_channel(1289772928082378852)

                # Check if owner is None
                if owner is None:
                    owner_info = "Owner not found"
                else:
                    owner_info = f"{owner}({owner.id})"

                embed = Embed(
                    title="Beta bot added to a guild",
                    description=f"**NAME:** `{guild.name}`\n**ID:** `{id}`\n**OWNER:** `{owner_info}`\n**IS_DEV_GUILD:** `{is_dev_guild}`"
                )

                if not is_dev_guild:
                    await guild.leave()
                    await channel.send(embed=embed)
                    


        @commands.Cog.listener()
        async def on_guild_join(self, guild: discord.Guild):
            id = guild.id
            owner = guild.get_member(guild.owner_id)
            is_dev_guild = id in self.beta_guilds
            channel = self.merx.get_guild(self.beta_guilds[0]).get_channel(1289772928082378852)

            # Check if owner is None
            if owner is None:
                owner_info = "Owner not found"
            else:
                owner_info = f"{owner}({owner.id})"

            embed = Embed(
                title="Beta bot added to a guild",
                description=f"**NAME:** `{guild.name}`\n**ID:** `{id}`\n**OWNER:** `{owner_info}`\n**IS_DEV_GUILD:** `{is_dev_guild}`"
            )

            if not is_dev_guild:
                await guild.leave()
            
            await channel.send(embed=embed)



    # This updated the guilds and users periodically every 30 seconds.

    @tasks.loop(seconds=30)
    async def change_status(self):
        guild_count = len(self.merx.guilds)
        user_count = sum(guild.member_count for guild in self.merx.guilds)


        await self.merx.change_presence(activity=discord.Activity(
            name=f"{guild_count} Guilds • {user_count:,} Users • /help",
            type=discord.ActivityType.watching
        ))
            


    if constants.merx_environment_type() == "Production":
        @commands.Cog.listener()
        async def on_member_join(self, member: discord.Member):
            welcome_channel = discord.utils.get(member.guild.text_channels, name=CHANNEL_NAME_FOR_WELCOME)
            welcome_channel = None
            for channel_name in CHANNEL_NAME_FOR_WELCOME:
                welcome_channel = discord.utils.get(member.guild.text_channels, name=channel_name)
                if welcome_channel:
                    break
            
            if welcome_channel:
                member_count = member.guild.member_count
                await welcome_channel.send(f"{member.mention} Welcome to **{member.guild.name}**! Feel free to explore. We now have **{member_count}** members. 🎉")         
    


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