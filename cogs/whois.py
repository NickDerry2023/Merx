import discord
from discord.ext import commands
from utils.constants import MerxConstants
from utils.embeds import UserInformationEmbed

constants = MerxConstants()


class WhoisCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()

    @commands.hybrid_command(description="Show all information about a certain user.", with_app_command=True, extras={"category": "General"})
    async def whois(self, ctx, member: discord.User = None):
        try:
            fetched_member: discord.Member = await self.merx.fetch_user(member.id)
        except Exception as e:
            raise commands.CommandInvokeError(e)
        
        try:
            fetched_member: discord.Member = await ctx.guild.fetch_member(fetched_member.id)
        except Exception:
            pass
        
        embed = await UserInformationEmbed(fetched_member, self.constants, self.merx).create_embed()

        await ctx.send(embed=embed)
    
async def setup(merx):
    await merx.add_cog(WhoisCommandCog(merx))