import discord
import asyncio
import uuid
import shortuuid
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import ErrorEmbed, PermissionDeniedEmbed, UserInformationEmbed


constants = MerxConstants()


class WhoisCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()



    @commands.hybrid_command(description="Check to see information about users and bots.", with_app_command=True, extras={"category": "General"})
    async def whois(self, ctx, member: discord.Member = None):


        member = member or ctx.author
        
        
        embed = UserInformationEmbed(member, self.constants).create_embed()


        await ctx.send(embed=embed)
    


async def setup(merx):
    await merx.add_cog(WhoisCommandCog(merx))