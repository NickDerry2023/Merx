import discord
import uuid
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import PermissionDeniedEmbed

constants = MerxConstants()

class KickCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx



    @commands.hybrid_command(description="You can run this command to kick a user in your server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        
    
        mongo_db = await constants.mongo_setup()
        

        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return
        
        
        kick_collection = mongo_db["kicks"]
        

        if not ctx.author.guild_permissions.kick_members:
            await ctx.send(embed=PermissionDeniedEmbed())
            return
        
        
        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to manage messages.")
            return
        
        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to kick members.")
            return
        
        
        case_number = f"Case #{str(uuid.uuid4().int)[:4]}"

        try:
            await member.kick(reason=reason)
        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to kick that user.")
            return
        except discord.HTTPException:
            await ctx.send("<:xmark:1285350796841582612> I couldn't kick this user.")
            return

        try:
            dm_message = f"<:whitecheck:1285350764595773451> **{case_number} - You have been kicked from **{ctx.guild.name}** for {reason}"
            await member.send(dm_message)
        except discord.Forbidden:
            await ctx.send(f"<:xmark:1285350796841582612> Unable to send a DM to {member.mention}; kicking the user in the server.")


        kick_entry = {
            "case_number": case_number,
            "guild_id": ctx.guild.id,
            "guild_name": ctx.guild.name,
            "kicked_user_id": member.id,
            "kicked_user_name": str(member),
            "kicked_by_id": ctx.author.id,
            "kicked_by_name": str(ctx.author),
            "reason": reason,
            "timestamp": ctx.message.created_at.isoformat()
        }
        kick_collection.insert_one(kick_entry)
        

        await ctx.send(f"<:whitecheck:1285350764595773451> **{case_number} - {member}** has been kicked for {reason}.")

async def setup(merx):
    await merx.add_cog(KickCommandCog(merx))