import discord
import os
import requests
import asyncio
from datetime import datetime
from discord.ext import commands
from cogs.utils.constants import MerxConstants


# Sets bots constants
# We use constants.py to specify things like the mongo db connnection, prefix
# and default embed color.

constants = MerxConstants()


class Merx(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = None
        self.start_time = datetime.utcnow()
        
        
        
    async def is_owner(self, user: discord.User):
        
        # Use bypassed users from the constants class instead of hardcoding them
        
        constants = MerxConstants()
        await constants.call_mongo_run()
        
        # Check if the user ID is in the bypassed users list
        
        if user.id in constants.bypassed_users:
            return True
        return False



    # Sets up the cogs for Merx.
    
    async def setup_hook(self) -> None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.load_extension('cogs.utils.hot_reload')
        print('All cogs loaded successfully!')


# Sets the bot's intents.

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# Set bot prefix

prefix =  constants.prefix_setup()


merx = Merx(command_prefix=prefix,
            intents=intents,
            chunk_guilds_at_startup=False,
            help_command=None,
            allowed_mentions=discord.AllowedMentions(replied_user=True, everyone=True, roles=True))


# Before invoking any command, check blacklist.

@merx.before_invoke
async def before_invoke(ctx):

    if ctx.author.id in constants.bypassed_users:
        return


    # User blacklist check
    
    if ctx.command.name != "unblacklist":
        if ctx.author.id in constants.blacklists:
            em = discord.Embed(
                title="Blacklisted",
                description="You are blacklisted from Merx - please appeal within our [support server](https://discord.gg/nAX4yhVEgy)!.",
                color=discord.Color(int('fecb02', 16)),
            )
            await ctx.send(embed=em)
            raise commands.CheckFailure("Blacklisted")



    # Server blacklist check
    
    if ctx.command.name != "guild_unblacklist":
        if ctx.guild.id in constants.server_blacklists:
            em = discord.Embed(
                title="Blacklisted Guild",
                description="This server is blacklisted from Merx - please appeal within our [support server](https://discord.gg/nAX4yhVEgy)!",
                color=discord.Color(int('fecb02', 16)),
            )
            await ctx.send(embed=em)
            raise commands.CheckFailure("Blacklisted")



    if ctx.channel.type == discord.ChannelType.private:
        raise commands.NoPrivateMessage("This command cannot be used in private messages.")



merx.run(constants.merx_token_setup())
