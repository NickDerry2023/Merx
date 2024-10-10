import discord
import shortuuid
from discord.ext import commands
 
from utils.constants import MerxConstants

constants = MerxConstants()


class SayCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    # This is a say command that allows users to say things using the bot.

    @commands.hybrid_command(description="Use this command to say things to people using the bot.", with_app_command=True, extras={"category": "General"})
    async def say(self, ctx, *, message: str):
 
        if ctx.interaction:
            await ctx.send("sent", allowed_mentions=discord.AllowedMentions.none(), ephemeral=True)
            await ctx.channel.send(message, allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.channel.send(message, allowed_mentions=discord.AllowedMentions.none())
            await ctx.message.delete()
            
            

async def setup(merx):
    await merx.add_cog(SayCommandCog(merx))
