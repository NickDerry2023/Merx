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
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def purge(self, ctx, option: str, limit: int, *, user: discord.User = None):
        
        if hasattr(ctx, "interaction") and ctx.interaction is not None:
            await ctx.interaction.response.defer()


        if limit < 1:
            await ctx.send("Please specify a valid number of messages to delete (greater than 0).")
            return
        
        
        if option.lower() not in ["all", "bots", "user", "merx"]:
            await ctx.send("Invalid option! Use `all`, `bots`, `user`, or `merx`.")
            return


        try:
            if option.lower() == "all":
                
                
                deleted = await ctx.channel.purge(limit=limit)
                
                
                embed = SuccessEmbed(
                    title="Messages Cleared",
                    description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} messages from this channel."
                )
            
            
            elif option.lower() == "bots":
                
                
                deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.bot)
                
                
                embed = SuccessEmbed(
                    title="Bot Messages Cleared",
                    description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} bot messages from this channel."
                )
            
            
            elif option.lower() == "user":
                
                
                if user is None:
                    await ctx.send("Please specify a user to purge messages from.")
                    return
                
                
                deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.id == user.id)
                
                
                embed = SuccessEmbed(
                    title="User Messages Cleared",
                    description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} messages from {user.mention}."
                )
            
            
            elif option.lower() == "merx":
                
                
                deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.id == self.merx.user.id)
                
                
                embed = SuccessEmbed(
                    title="Merx Messages Cleared",
                    description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} messages from Merx."
                )
                

            await ctx.send(embed=embed)
        
        
        except discord.Forbidden:
            await ctx.send(embed=ErrorEmbed())
            
            
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while trying to purge messages: {str(e)}")

        
        
        except discord.Forbidden:
            await ctx.send(embed=ErrorEmbed())
            
            
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while trying to purge messages: {str(e)}")
    
    
    
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
