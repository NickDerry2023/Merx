import discord
import time
import datetime
import subprocess
from datetime import datetime
from discord import Interaction
from discord.ext import commands
from utils.constants import MerxConstants, db
from utils.embeds import AboutEmbed, AboutWithButtons, PingCommandEmbed, ServerInformationEmbed


constants = MerxConstants()


# The main commands Cog.

class CommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        


    # This is the info Command for merx. Place every other command before this one, this should be the last command in
    # this file for readability purposes.

    @commands.hybrid_command(description="Provides important information about merx.", with_app_command=True, extras={"category": "Other"})
    async def about(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)
        
        
        # Try to delete the command message to clean up the discord response so that its not as messy
        
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass
        
        # Collect information for the embed such as the bots uptime, hosting information, database information
        # user information and server information so that users can see the growth of the bot.
        
        uptime_seconds = getattr(self.merx, 'uptime', 0)
        uptime_formatted = f"<t:{int((self.merx.start_time.timestamp()))}:R>"
        guilds = len(self.merx.guilds)
        users = sum(guild.member_count for guild in self.merx.guilds)
        version_info = await db.command('buildInfo')
        version = version_info.get('version', 'Unknown')
        shards = self.merx.shard_count or 1
        cluster = 0
        environment = constants.merx_environment_type()
        
        
        # Formats the date and time
        
        command_run_time = datetime.now()
        formatted_time = command_run_time.strftime("Today at %I:%M %p UTC")


        # This builds the emebed.

        embed = AboutEmbed.create_info_embed(
            uptime=self.merx.start_time,
            guilds=guilds,
            users=users,
            latency=self.merx.latency,
            version=version,
            bot_name=ctx.guild.name,
            bot_icon=ctx.guild.icon,
            shards=shards,
            cluster=cluster,
            environment=environment,
            command_run_time=formatted_time,
            thumbnail_url="https://cdn.discordapp.com/avatars/1285105979947749406/3a8b148f12e07c1d83c32d4ed26f618e.png"
        )


        # Send the emebed to view.

        view = AboutWithButtons.create_view()

        await ctx.send(embed=embed, view=view)
        
        
        
    # This is a server information command that will show information about a server
    # in an easy to read emebed similar to circle bot.
    
    @commands.hybrid_command(description="Displays information about the current server.", with_app_command=True, extras={"category": "General"})
    async def serverinfo(self, ctx):


        embed = ServerInformationEmbed(ctx.guild, constants).create_embed()

        if isinstance(ctx, Interaction):
            
            await ctx.response.send_message(embed=embed)
            
        elif isinstance(ctx, commands.Context):
            
            await ctx.send(embed=embed)
            
            
            
    # This will get the version information from GitHub directly. This is so we dont have to change it
    # each time as that will get anoying fast and I am a lazy developer.
     
    def get_git_version(self):
        try:
            version = subprocess.check_output(['git', 'describe', '--tags']).decode('utf-8').strip()

            commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()

            return f"{version} ({commit})"
        
        except subprocess.CalledProcessError:
            return "Unknown Version"       
            
            
    # This gets the MongoDB latency using a lightweight command like ping and then mesuring its response time.        
            
    async def get_mongo_latency(self):
        try:
            start_time = time.time()
            
            
            await db.command('ping')


            mongo_latency = round((time.time() - start_time) * 1000)
            return mongo_latency


        except Exception as e:
            print(f"Error measuring MongoDB latency: {e}")
            return -1
    
            
    
    # This is the space for the ping command which will allow users to ping.
    
    @commands.hybrid_command(name="ping", description="Check the bot's latency and uptime.", with_app_command=True, extras={"category": "Other"})
    async def ping(self, ctx: commands.Context):
        
        
        latency = self.merx.latency
        
        database_latency = await self.get_mongo_latency()


        # Calculate uptime
        
        uptime_seconds = getattr(self.merx, 'uptime', 0)
        uptime_formatted = f"<t:{int((self.merx.start_time.timestamp()))}:R>"


        # Define the bot version
        
        version = self.get_git_version()


        # Use the embed creation function from embeds.py
        
        embed = PingCommandEmbed.create_ping_embed(
            latency=latency,
            database_latency=database_latency,
            uptime=self.merx.start_time,
            version=version
        )
        

        await ctx.send(embed=embed)


async def setup(merx):
    await merx.add_cog(CommandsCog(merx))
