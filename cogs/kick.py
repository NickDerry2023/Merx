import discord
import uuid
from discord.ext import commands
from utils.constants import cases
from utils.utils import get_next_case_id
import time

class KickCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx

    @commands.hybrid_command(description="You can run this command to kick a user in your server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to manage messages.")
            return
        
        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to kick members.")
            return

        try:
            await member.kick(reason=reason)
        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to kick that user.")
            return
        except discord.HTTPException:
            await ctx.send("<:xmark:1285350796841582612> I couldn't kick this user.")
            return

        case_id = await get_next_case_id(ctx.guild.id)

        try:
            dm_message = f"<:whitecheck:1285350764595773451> **Case #{case_id} - You have been kicked from **{ctx.guild.name}** for {reason}"
            await member.send(dm_message)
        except discord.Forbidden:
            await ctx.send(f"<:xmark:1285350796841582612> Unable to send a DM to {member.mention}; kicking the user in the server.")


        kick_entry = {
            "case_id": case_id,
            "guild_id": ctx.guild.id,
            "user_id": member.id,
            "moderator_id": ctx.author.id,
            "reason": reason,
            "timestamp": int(time.time()),
            "type": "kick",
            "status": "active"
        }
        await cases.insert_one(kick_entry)
        

        await ctx.send(f"<:whitecheck:1285350764595773451> **Case #{case_id} - {member}** has been kicked for {reason}.")

async def setup(merx):
    await merx.add_cog(KickCommandCog(merx))