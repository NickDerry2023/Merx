import discord
from datetime import datetime
from discord.ext import commands
from utils.constants import MerxConstants, cases

class CaseSearchCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()  # Access constants for MongoDB setup

    @commands.hybrid_group(description="Group command")
    async def case(self, ctx):
        return
    
    @case.command(description="Searches cases by an Case ID.", with_app_command=True)
    async def view(self, ctx: commands.Context, *, caseid: int):
        case_info = await cases.find_one({'case_id': caseid, 'guild_id': ctx.guild.id})
        if case_info:
            embed = discord.Embed(title=f"Case ID: {case_info.get('case_id')} | {case_info.get('type').title()}", 
                                description=f"Status: **{case_info.get('status').title()}**\nUser: <@{case_info.get('user_id')}>\nModerator: <@{case_info.get('moderator_id')}>\nTimestamp: <t:{case_info.get('timestamp')}:F>\nReason: {case_info.get('reason')}",
                                color=self.constants.merx_embed_color_setup())
            member: discord.Member = await self.merx.fetch_user(case_info.get('user_id'))
            try:
                embed.set_author(name=f"{member.name}\'s Case", icon_url=member.avatar.url)
            except:
                embed.set_author(name=f"{member.name}\'s Modlogs", icon_url=member.default_avatar.url)
            await ctx.send(embed=embed)
        elif not case_info:
            await ctx.send(f"**{caseid}** could not be found!")
    
    @case.command(description="Void/Clear a case by ID", with_app_command=True)
    async def void(self, ctx: commands.Context, *, caseid: int):
        case_info = await cases.find_one_and_update({'case_id': caseid, 'guild_id': ctx.guild.id}, {'$set': {'status': 'cleared'}})
        if case_info:
            await ctx.send(f"Case ID: {caseid} has been voided!")
        elif not case_info:
            await ctx.send(f"Case ID: {caseid} could not be found!")


async def setup(merx):
    await merx.add_cog(CaseSearchCog(merx))
