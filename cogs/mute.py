import discord
import uuid
from discord.ext import commands
from utils.constants import cases
from utils.utils import get_next_case_id
from datetime import timedelta

class MuteCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    @commands.hybrid_command(description="Mute/Timeout a certain user", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
        if member == ctx.author:
            return await ctx.send("<:xmark:1285350796841582612> You cannot mute yourself!")
    
        elif member == ctx.guild.me:
            return await ctx.send("<:xmark:1285350796841582612> I cannot mute myself!")
        
        try:
            if member.top_role >= ctx.author.top_role:
                return await ctx.send("You cannot mute a member with an equal or higher role!")
        except AttributeError:
            pass

        until = discord.utils.utcnow() + timedelta(minutes=minutes)

        await member.timeout(until, reason=reason)
        
        await ctx.send(f"**{member.name}** has been muted for {minutes} minutes!")

    @commands.hybrid_command(description="Remove timeout from a certain user", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        if member == ctx.author:
            return await ctx.send("<:xmark:1285350796841582612> You cannot unmute yourself!")
    
        elif member == ctx.guild.me:
            return await ctx.send("<:xmark:1285350796841582612> I cannot unmute myself!")
        
        try:
            if member.top_role >= ctx.author.top_role:
                return await ctx.send("You cannot unmute a member with an equal or higher role!")
        except AttributeError:
            pass

        await member.timeout(None, reason=reason)
        await ctx.send(f"**{member.name}** has been unmuted!")



async def setup(merx):
    await merx.add_cog(MuteCommandCog(merx))