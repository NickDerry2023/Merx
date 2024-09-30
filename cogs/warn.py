import discord
import asyncio
import uuid
import shortuuid
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import PermissionDeniedEmbed
from cogs.utils.errors import send_error_embed


constants = MerxConstants()


class WarnCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()


    @commands.hybrid_command(description="You can run this command to warn a user in your server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        mongo_db = await self.constants.mongo_setup()


        if mongo_db is None:
            
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return
        
        
        
        warn_collection = mongo_db["warns"]



        # Check if the user has administrator permissions
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=PermissionDeniedEmbed())
            return



        # Check if the bot has permissions to manage messages
        
        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to manage messages.")
            return


        # Generate a unique case number
        
        case_number = f"Case #{str(uuid.uuid4().int)[:4]}"



        # Sends a DM to the user
        
        try:
            dm_message = f"<:warning:1285350764595773451> **{case_number} - You have been warned in {ctx.guild.name}** for {reason}."
            await member.send(dm_message)
        except discord.Forbidden:
            await ctx.send(f"<:xmark:1285350796841582612> Unable to send a DM to {member.mention}; warning the user in the server.")



        # Log to MongoDB, This will put the warning into the database.
        
        warn_entry = {
            "case_number": case_number,
            "guild_id": ctx.guild.id,
            "guild_name": ctx.guild.name,
            "warned_user_id": member.id,
            "warned_user_name": str(member),
            "warned_by_id": ctx.author.id,
            "warned_by_name": str(ctx.author),
            "reason": reason,
            "timestamp": ctx.message.created_at.isoformat()
        }
        warn_collection.insert_one(warn_entry)


        await ctx.send(f"<:warning:1285350764595773451> **{case_number} - {member}** has been warned for {reason}.")



async def setup(merx):
    await merx.add_cog(WarnCommandCog(merx))