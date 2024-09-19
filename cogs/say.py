import discord
import asyncio
import uuid
import shortuuid
from discord.ext import commands
from cogs.utils.embeds import ErrorEmbed
from cogs.utils.errors import send_error_embed
from cogs.utils.constants import MerxConstants


constants = MerxConstants()


class SayCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    # This is a say command that allows users to say things using the bot.

    @commands.hybrid_command(description="Use this command to say things to people using the bot.", with_app_command=True, extras={"category": "General"})
    async def say(self, ctx, *, message: str):
        
        try:
            await ctx.send(message)
        except Exception as e:
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(interaction, e, error_id)
            
            

async def setup(merx):
    await merx.add_cog(SayCommandCog(merx))
