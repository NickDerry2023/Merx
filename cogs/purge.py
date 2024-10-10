import discord
from discord.ext import commands
from utils.embeds import SuccessEmbed
 
from utils.constants import MerxConstants


constants = MerxConstants()


class ClearChatCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.cooldown = 2 
    
    
    # Purge command to purge user messages from discord channels.
    
    @commands.hybrid_command(name="purge", description="Clear a large number of messages from the current channel.", with_app_command=True, extras={"category": "General"})
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def purge(self, ctx, option: str = None, limit: int = None, *, user: discord.User = None):
        if hasattr(ctx, "interaction") and ctx.interaction is not None:
            await ctx.interaction.response.defer()


        if option is not None and option.isdigit():
            limit = int(option)
            option = "any"
        


        if option is None and limit is not None:
            option = "any"
        


        if limit is None or limit < 1:
            await ctx.send("Please specify a valid number of messages to delete (greater than 0).")
            return


        option = option.lower()
        

        if option == "any":
            deleted = await ctx.channel.purge(limit=limit)
            embed = SuccessEmbed(
                title="Messages Cleared",
                description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} messages from this channel."
            )


        elif option == "bots":
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.bot)
            embed = SuccessEmbed(
                title="Bot Messages Cleared",
                description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} bot messages from this channel."
            )


        elif option == "user":
            if user is None:
                await ctx.send("Please specify a user to purge messages from.")
                return
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.id == user.id)
            embed = SuccessEmbed(
                title="User Messages Cleared",
                description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} messages from {user.mention}."
            )


        elif option == "merx":
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.id == self.merx.user.id)
            embed = SuccessEmbed(
                title="Merx Messages Cleared",
                description=f"<:whitecheck:1285350764595773451> Cleared {len(deleted)} messages from Merx."
            )


        else:
            await ctx.send("Please specify a valid option: any, bots, user, or merx.")
            return


        await ctx.send(embed=embed)
    
    
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



async def setup(merx):
    await merx.add_cog(ClearChatCog(merx))
