import discord
from discord.ext import commands
from cogs.utils.errors import send_error_embed
from cogs.utils.embeds import DebugEmbed, PermissionDeniedEmbed


# This is the admins cog for the bots admin commands that only server admins may run.
# This includes a debug command to debug the bot.

class AdminCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    @commands.hybrid_command(name="debug", description="Displays debug information for the Merx.", with_app_command=True, extras={"category": "Debugging"})
    async def debug(self, ctx: commands.Context):
        
        
        # Displays debugging information.
        # Check if the user has administrator permissions
        
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=PermissionDeniedEmbed())
            return


        # Send the embed with debugging information
        
        await ctx.send(embed=DebugEmbed(self.merx, ctx))



async def setup(merx):
    await merx.add_cog(AdminCommandsCog(merx))