import discord
import asyncio
import uuid
from discord.ext import commands
from utils.constants import cases
from utils.utils import get_next_case_id
import time

class BanCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
    
    @commands.hybrid_command(name="ban", description="Ban command to ban members from your server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.User, *, reason: str = "Nothing was provided"):
        try:
            fetched_member: discord.Member = await self.merx.fetch_user(member.id)
        except Exception as e:
            raise commands.CommandInvokeError(e)
        
        
        banned_users = ctx.guild.bans()
        user_to_unban = None
        
        
        async for ban_entry in banned_users:
            if ban_entry.user.id == fetched_member.id:
                user_to_unban = ban_entry.user
                break


        # Moved the error checking to the top to prevent as many nested if statements.

        if user_to_unban:
            return await ctx.send(f"<:xmark:1285350796841582612> User {fetched_member} is already banned.", ephemeral=True)
        
        
        elif fetched_member == ctx.author:
            return await ctx.send("<:xmark:1285350796841582612> You cannot ban yourself!")
    
    
        elif fetched_member == ctx.guild.me:
            return await ctx.send("<:xmark:1285350796841582612> I cannot ban myself!")
        
        
        try:
            if fetched_member.top_role >= ctx.author.top_role:
                return await ctx.send("You cannot ban a member with an equal or higher role!")
            
            
        except AttributeError:
            pass
         
        # Sends a DM to the user
        
        case_id = await get_next_case_id(ctx.guild.id)

        try:
            dm_message = f"<:whitecheck:1285350764595773451> **{case_id} - You have been banned from {ctx.guild.name}** for {reason}."
            await fetched_member.send(dm_message)
        except discord.Forbidden:
            await ctx.send(f"<:xmark:1285350796841582612> Unable to send a DM to {fetched_member.mention}; proceeding with the ban.")


        # Perform the ban operation
        try:
            await ctx.guild.ban(fetched_member, reason=reason)
        except Exception as e:
            raise commands.CommandInvokeError(e)
        
        # Log to MongoDB
        
        ban_entry = {
            "case_id": case_id,
            "guild_id": ctx.guild.id,
            "user_id": member.id,
            "moderator_id": ctx.author.id,
            "reason": reason,
            "timestamp": int(time.time()),
            "type": "ban",
            "status": "active"
        }
        await cases.insert_one(ban_entry)

        # Send the success message
        
        await ctx.send(f"<:whitecheck:1285350764595773451> **{case_id} - {member}** has been banned for {reason}.")
            
            
            
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
            await ctx.send(f"<:whitecheck:1285350764595773451> **Case #{case_number} - Successfully unbanned {user_to_unban.mention}** for: {reason}.", ephemeral=True)


        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I do not have permissions to unban this user.", ephemeral=True)
            
        
        
    # Softban command that bans and unbans a user, effectively deleting their messages.
    
    @commands.hybrid_command(description="Softban a user, deleting their messages from the server.", with_app_command=True, extras={"category": "Moderation"})
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        

        await ctx.guild.ban(member, reason=reason, delete_message_days=1)
        case_number = f"Case #{str(uuid.uuid4().int)[:4]}"  # Generate a short unique case number
        await ctx.send(f"<:whitecheck:1285350764595773451> **Case #{case_number} - Successfully softbanned {member.mention}** for: {reason}")
        await asyncio.sleep(2)
        await ctx.guild.unban(member)
        
        
        
async def setup(merx):
    await merx.add_cog(BanCommandCog(merx))
