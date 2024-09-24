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
    async def on_ready(self):
        guild_count = len(self.merx.guilds)
        user_count = sum(guild.member_count for guild in self.merx.guilds)


        await self.merx.change_presence(activity=discord.Activity(
            name=f"{guild_count} Guilds • {user_count:,} Users • /help",
            type=discord.ActivityType.watching
        ))
        

        print(f"{self.merx.user.name} is ready with {guild_count} guilds and {user_count:,} users.")
            

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
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



    async def global_blacklist_check(ctx):
    
    
    constants = ctx.bot.constants
    

    # Fetch blacklist if not already fetched or periodically
    
    if not constants.blacklists:
        await constants.fetch_blacklisted_users()

    if not constants.server_blacklists:
        await constants.fetch_blacklisted_guilds()


    # Check if the user is blacklisted
    
    if ctx.author.id in constants.blacklists and ctx.command.name != "unblacklist":
        
        em = discord.Embed(
            title="Blacklisted",
            description="You are blacklisted from Merx - please appeal within our [support server](https://discord.gg/nAX4yhVEgy)!",
            color=discord.Color(int('fecb02', 16)),
        )
        
        await ctx.send(embed=em)
        
        raise commands.CheckFailure("You are blacklisted from using this bot.")


    # Check if the guild is blacklisted
    
    if ctx.guild and ctx.guild.id in constants.server_blacklists and ctx.command.name != "guild_unblacklist":
        
        em = discord.Embed(
            title="Blacklisted Guild",
            description="This server is blacklisted from Merx - please appeal within our [support server](https://discord.gg/nAX4yhVEgy)!",
            color=discord.Color(int('fecb02', 16)),
        )
        
        await ctx.send(embed=em)
        
        raise commands.CheckFailure("This guild is blacklisted from using the bot.")


    # Prevent the command from being run in DMs
    
    if ctx.guild is None:
        raise commands.NoPrivateMessage("This command cannot be used in private messages.")

    return True




    # Before invoking any command, check blacklist.

    async def before_invoke(ctx):
        # Skip check if the user is in the bypass list
        if ctx.author.id in constants.bypassed_users:
            return
        # Run the blacklist check
        await global_blacklist_check(ctx)


    # These are the cog error handlers they determine how the error is sent.

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.handle_error(ctx, error.original if isinstance(error, commands.CommandInvokeError) else error)


    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        await self.handle_error(interaction, error)
        
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You are blacklisted and cannot use this command.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages.")
        else:
            # Handle other errors
            pass


async def setup(merx):
  await merx.add_cog(MerxEvents(merx))