import discord
import platform
from discord import Interaction
from discord.ext import commands
from discord.ui import View, Button
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import AboutEmbed, AboutWithButtons


class CommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()

        

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
        
        
        mongo_db = await self.constants.mongo_setup()
        
        # Collect information for the embed such as the bots uptime, hosting information, database information
        # user information and server information so that users can see the growth of the bot.
        
        uptime_seconds = getattr(self.merx, 'uptime', 0)
        uptime_formatted = f"<t:{int((self.merx.start_time.timestamp()))}:R>"
        guilds = len(self.merx.guilds)
        users = sum(guild.member_count for guild in self.merx.guilds)
        version = "Unknown"


        embed = AboutEmbed.create_info_embed(
            uptime=self.merx.start_time,
            guilds=guilds,
            users=users,
            latency=self.merx.latency,
            version=version,
            bot_name=ctx.guild.name,
            bot_icon=ctx.guild.icon,
            thumbnail_url="https://cdn.discordapp.com/avatars/1285105545078116453/605985a7a70fb5efbdfc3005c246a0cc.png"
        )

        view = AboutWithButtons.create_view()

        await ctx.send(embed=embed, view=view)


async def setup(merx):
    await merx.add_cog(CommandsCog(merx))
