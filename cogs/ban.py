import discord
import asyncio
import uuid
import shortuuid
from discord.ext import commands
from cogs.utils.embeds import DebugEmbed
from cogs.utils.constants import MerxConstants


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
        
        bans = mongo_db["bans"]
        
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
        
        case_number = f"Case #{str(uuid.uuid4().int)[:4]}"  # Generate a short unique case number
        
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
            bans.insert_one(ban_entry)

            # Send the success message
            
            await ctx.send(f"<:whitecheck:1285350764595773451> **{case_number} - {member}** has been banned for {reason}.")
        
        
        except discord.Forbidden:
            await ctx.send(embed=PermissionDeniedEmbed())
            return
        
        
        except discord.HTTPException:
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(interaction, e, error_id)
            
            
            
    @commands.hybrid_command(name="unban", description="Unban command to unban members from your server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User, *, reason: str = "No reason provided"):
        
        # Defer the response to avoid delay issues.
        
        await ctx.defer()

        try:
            
            # This command was hell to write.
            # Use async for to iterate over the banned users (since it's an async generator).
            
            banned_users = ctx.guild.bans()  # Don't await here, just call it.

            user_to_unban = None


            # Iterate asynchronously through the banned users list.
            
            async for ban_entry in banned_users:
                if ban_entry.user.id == user.id:
                    user_to_unban = ban_entry.user
                    break


            if user_to_unban is None:
                await ctx.send(f"<:xmark:1285350796841582612> User {user} is not banned.", ephemeral=True)
                return


            await ctx.guild.unban(user_to_unban, reason=reason)
            case_number = f"Case #{str(uuid.uuid4().int)[:4]}"  # Generate a short unique case number
            await ctx.send(f"<:whitecheck:1285350764595773451> **{case_number} - Successfully unbanned {user_to_unban.mention}** for: {reason}.", ephemeral=True)


        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I do not have permissions to unban this user.", ephemeral=True)
            
        
        
    # Softban command that bans and unbans a user, effectively deleting their messages.
    
    @commands.hybrid_command(description="Softban a user, deleting their messages from the server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        
        
        try:

            await ctx.guild.ban(member, reason=reason, delete_message_days=1)
            case_number = f"Case #{str(uuid.uuid4().int)[:4]}"  # Generate a short unique case number
            await ctx.send(f"<:whitecheck:1285350764595773451> **{case_number} - Successfully softbanned {member.mention}** for: {reason}")
            await asyncio.sleep(2)
            await ctx.guild.unban(member)


        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I do not have permission to ban this user.")
        except discord.HTTPException as e:
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(ctx, e, error_id)



    @softban.error
    async def softban_error(self, ctx, error):
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("<:xmark:1285350796841582612> You do not have the required permissions to softban members.")
            
            
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("<:xmark:1285350796841582612> I do not have the required permissions to softban members.")
            
            
        else:
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(ctx, error, error_id)
        
        
        
async def setup(merx):
    await merx.add_cog(BanCommandCog(merx))
