import discord
from discord.ext import commands
from datetime import datetime
from utils.constants import MerxConstants, cases

class ModLogsCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()

    @commands.hybrid_group(description="Group command")
    async def modlogs(self, ctx: commands.Context):
        return
    
    @modlogs.command(description="View all modlogs for certain user", with_app_command=True, extras={"category": "Moderation"})
    async def view(self, ctx, member: discord.Member):  
        number = 0
        
        embed = discord.Embed(title=f"", description="", color=self.constants.merx_embed_color_setup(), timestamp=datetime.utcnow())
        results = cases.find({'user_id': member.id, "guild_id": ctx.guild.id})
        async for result in results:
            if result.get('status') == "active":
                number += 1
                embed.add_field(name=f"Case ID: {result.get('case_id')} | {result.get('type').title()}", value=f"Reason: {result.get('reason')}\nModerator: <@{result.get('moderator_id')}> ({result.get('moderator_id')})\nDate: <t:{result.get('timestamp')}:F>", inline=False)
        
        if number == 0:
            embed = discord.Embed(title="Not Found", description="No mod logs could be found for this user!", color=self.constants.merx_embed_color_setup())
        else:
            try:
                embed.set_author(name=f"{member.name}\'s Modlogs", icon_url=member.avatar.url)
            except:
                embed.set_author(name=f"{member.name}\'s Modlogs", icon_url=member.default_avatar.url)
            embed.set_footer(text=f"ID: {member.id} • Total Modlogs: {number}")
        await ctx.send(embed=embed)

    @modlogs.command(description="Transfer all modlogs to a different user", with_app_command=True, extras={"category": "Moderation"})
    async def transfer(self, ctx, olduser: discord.Member = None, newuser: discord.Member = None): 
        results = cases.find({'user_id': olduser.id, "guild_id": ctx.guild.id})
        async for result in results:
            is_deleted = await cases.find_one_and_update({'case_id': result.get('case_id'), 'user_id': result.get('user_id'), 'guild_id': result.get('guild_id')}, {'$set': {'user_id': newuser.id}})
            if not is_deleted:
                await ctx.send(f"{result.get('case_id')} was not able to be updated!")
        await ctx.send(f"All moderation logs for **{olduser.name}** have been transfered to **{newuser}**")
    
    @modlogs.command(description="Clear all modlogs for a certain user", with_app_command=True, extras={"category": "Moderation"})
    async def clear(self, ctx, member: discord.Member = None):
        results = cases.find({'user_id': member.id, "guild_id": ctx.guild.id})
        async for result in results:
            case_info = await cases.find_one_and_update({'case_id': result.get('case_id'), 'guild_id': ctx.guild.id}, {'$set': {'status': 'cleared'}})
            if not case_info:
                await ctx.send(f"{result.get('case_id')} was not able to be deleted!")

        await ctx.send(f"All moderation logs have been cleared for **{member.name}**.")



async def setup(merx):
    await merx.add_cog(ModLogsCommandCog(merx))