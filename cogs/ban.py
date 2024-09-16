import discord
from discord.ext import commands
from cogs.utils.errors import send_error_embed
from cogs.utils.embeds import DebugEmbed, PermissionDeniedEmbed
from cogs.utils.constants import MerxConstants
import uuid

# This is the admins cog for the bots admin commands that only server admins may run.
# This includes a ban command to ban members from your server.

class BanCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()

    
    @commands.hybrid_command(name="ban", description="Ban command to ban members from your server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        
        mongo_db = await self.constants.mongo_setup()

        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return
        
        ban_collection = mongo_db["ban_collection"]
        
        # Bans a member from the server with an optional reason.
        # Check if the user has administrator permissions
        
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=PermissionDeniedEmbed())
            return


        # Check if the bot has permissions to ban members
        
        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.send(
                "I do not have permission to ban members.",
                color=discord.Color.red()
            )
            return


        # Check if the member to ban is the bot or the command issuer
        
        if member == ctx.author:
            await ctx.send("<:xmark:1285350796841582612> You cannot ban yourself!")
            return

        if member == ctx.guild.me:
            await ctx.send("<:xmark:1285350796841582612> I cannot ban myself!")
            return


        # Check if the target member has a higher or equal role
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You cannot ban a member with an equal or higher role!")
            return


        # Generate a unique case number
        
        case_number = f"Case #{str(uuid.uuid4().int)[:8]}"  # Generate a short unique case number
        
        # Sends a DM to the user
        
        try:
            dm_message = f"<:whitecheck:1285350764595773451> **{case_number} - You have been banned from {ctx.guild.name}** for {reason}."
            await member.send(dm_message)
        except discord.Forbidden:
            await ctx.send(f"<:xmark:1285350796841582612> Unable to send a DM to {member.mention}; proceeding with the ban.")


        # Perform the ban operation
        
        try:
            await member.ban(reason=reason)
            
            # Log to MongoDB
            
            ban_entry = {
                "case_number": case_number,
                "guild_id": ctx.guild.id,
                "guild_name": ctx.guild.name,
                "banned_user_id": member.id,
                "banned_user_name": str(member),
                "banned_by_id": ctx.author.id,
                "banned_by_name": str(ctx.author),
                "reason": reason,
                "timestamp": ctx.message.created_at.isoformat()
            }
            ban_collection.insert_one(ban_entry)

            # Send the success message
            
            await ctx.send(f"<:whitecheck:1285350764595773451> **{case_number} - {member}** has been banned for {reason}.")
        
        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to ban this member.")
        except discord.HTTPException:
            await ctx.send("<:xmark:1285350796841582612> An error occurred while trying to ban the member.")
            
            
    @commands.hybrid_command(name="unban", description="Unban command to unban members from your server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        
        # Defer the response to avoid delay issues.
        
        await ctx.defer()


        try:
            
            # Try to unban the user by getting their ID from the ban list.
            
            banned_users = await ctx.guild.bans()
            user_to_unban = None

            # Iterate through banned users to find the correct one
            
            for ban_entry in banned_users:
                if ban_entry.user.id == user.id:
                    user_to_unban = ban_entry.user
                    break

            if user_to_unban is None:
                await ctx.send(f"<:xmark:1285350796841582612> User {user} is not banned.", ephemeral=True)
                return

            # Proceed with unbanning the user
            
            await ctx.guild.unban(user_to_unban, reason=reason)

            # Confirm the unban action
            
            case_number = f"Case #{str(uuid.uuid4().int)[:8]}"  # Generate a short unique case number
            
            
            
            await ctx.send(f"<:whitecheck:1285350764595773451> **{case_number} - Successfully unbanned {user_to_unban.mention}** for: {reason}.", ephemeral=True)



        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I do not have permissions to unban this user.", ephemeral=True)

        except discord.HTTPException as e:
            await ctx.send(f"<:xmark:1285350796841582612> Failed to unban the user. Error: {str(e)}", ephemeral=True)
    
    
    
async def setup(merx):
    await merx.add_cog(BanCommandCog(merx))
