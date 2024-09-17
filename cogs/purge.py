import discord
import asyncio
from discord.ext import commands
from cogs.utils.embeds import ErrorEmbed, PermissionDeniedEmbed, SuccessEmbed
from cogs.utils.errors import send_error_embed
from cogs.utils.constants import MerxConstants


constants = MerxConstants()


class ClearChatCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.cooldown = 2 
    
    
    # Purge command to purge user messages from discord channels.
    
    @commands.hybrid_command(name="purge", description="Clear a large number of messages from the current channel.", with_app_command=True, extras={"category": "General"})
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.user)  # Apply the cooldown here
    async def purge(self, ctx, amount: int):
        
        
        # This checks to see if the user specified the amount of messages to delete.
        # this prevents an empty number from being sent.
        
        if amount < 1:
            await ctx.send("Please specify a number of messages to delete.")
            return


        try:
            await ctx.channel.purge(limit=amount)
            
            embed = SuccessEmbed(
                title="Messages Cleared",
                description=f"Cleared {amount} messages from this channel."
            )
            
            await ctx.send(embed=embed)
        
        
        
        except discord.Forbidden:
            await ctx.send(embed=ErrorEmbed())
    
    
    
    # These are the cog error handlers they determine how the error is sent.
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Cooldown",
                description=f"You are running the command too fast! Please wait {self.cooldown} seconds before using this command again.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
            
            
    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        await self.handle_error(interaction, error)



async def setup(merx):
    await merx.add_cog(ClearChatCog(merx))
