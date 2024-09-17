import discord
import os
import requests
import asyncio
import sentry_sdk
from datetime import datetime
from discord.ext import commands
from cogs.utils.constants import MerxConstants


# We use constants.py to specify things like the mongo db connnection, prefix
# and default embed color.

constants = MerxConstants()


class Merx(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = None
        self.start_time = datetime.utcnow()
        
        
    # Use bypassed users from the constants class instead of hardcoding them
    # The constants.py file will get the IDs from MongoDb allowing bot owners
    # to remove and add users.
        
    async def is_owner(self, user: discord.User):
        if not constants.bypassed_users:
            await constants.fetch_bypassed_users()
        return user.id in constants.bypassed_users


    # Sets up the cogs for Merx. This will cycle thru the cogs folder and
    # load each file with the .py file extenstion.
    
    async def setup_hook(self) -> None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.load_extension('cogs.utils.hot_reload')
        print('All cogs loaded successfully!')


# Sets the bot's intents. This uses the members intent, default intents, and message_content
# intent. We will call intents later inorder to start Merx Bot.

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# Set bot prefix

prefix =  constants.prefix_setup()


# Intializes Merx Bot and loads the prefix, intents, and other important things for discord.

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
    # This is the unblacklist block to check if users are blacklisted and unblacklisted.
    
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


def run():
    
    # Sets up sentry for advanced error reporting. 
    # We use Cali Web Design's sentry account.
    
    sentry_sdk.init(
        dsn=constants.sentry_dsn_setup(),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    merx.run(constants.merx_token_setup())


if __name__ == "__main__":
    run()
