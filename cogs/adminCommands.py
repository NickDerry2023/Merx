import discord
import asyncio
import uuid
from discord.ext import commands
from cogs.utils.errors import send_error_embed
from cogs.utils.embeds import DebugEmbed, PermissionDeniedEmbed, ErrorEmbed
from cogs.utils.constants import MerxConstants


constants = MerxConstants()


# This is the admins cog for the bots admin commands that only server admins may run.
# This includes a debug command to debug the bot.

class AdminCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.merx.loop.create_task(constants.mongo_setup())



    @commands.hybrid_command(name="debug", description="Displays debug information for the Merx.", with_app_command=True, extras={"category": "Debugging"})
    async def debug(self, ctx: commands.Context):
        
        
        # Displays debugging information.
        # Check if the user has administrator permissions
        
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=PermissionDeniedEmbed())
            return


        # Send the embed with debugging information
        
        await ctx.send(embed=DebugEmbed(self.merx, ctx))
        
       
        
    # This command will add users into blacklist_bypass collection so they can run commands like JSK
    # and blacklist_guild or blacklist_user.
        
    @commands.hybrid_command(name="add_owner", description="Add a user to the bypassed list.", with_app_command=True, extras={"category": "Debugging"})
    @commands.has_permissions(administrator=True)
    async def add_owner(self, ctx: commands.Context, user: discord.User):
        
        
        # Check if the user is already in the bypass list
        
        if user.id in constants.bypassed_users:
            await ctx.send(f"<:xmark:1285350796841582612> {user.mention} is already in the bypass list.")
            return


        try:
            # Add the user to the MongoDB collection
            
            collection = constants.mongo_db["blacklist_bypass"]
            await collection.insert_one({"discord_id": user.id})
            
            
            # Fetch updated bypassed users list
            
            await constants.fetch_bypassed_users()
            await ctx.send(f"<:whitecheck:1285350764595773451> {user.mention} has been added to the bypass list. They can now run owner commands.")
            
            
        except Exception as e:
            embed = ErrorEmbed()
            await ctx.send(embed=embed)



    # This command will remove owners from the bypassed users and prevent them from using blacklist commands
    # or JSK commands. This is incase the developer or owner leaves or steps down.
    
    @commands.hybrid_command(name="remove_owner", description="Remove a user from the bypassed list.", with_app_command=True, extras={"category": "Debugging"})
    @commands.has_permissions(administrator=True)
    async def remove_owner(self, ctx: commands.Context, user: discord.User):
        
        # Always refresh the bypassed users list before performing the check
        
        await constants.fetch_bypassed_users()

        if user.id not in constants.bypassed_users:
            await ctx.send(f"<:xmark:1285350796841582612> {user.mention} is not in the bypass list.")
            return

        try:
            collection = constants.mongo_db["blacklist_bypass"]
            result = await collection.delete_one({"discord_id": user.id})
            
            if result.deleted_count == 0:
                await ctx.send(f"<:xmark:1285350796841582612> {user.mention} could not be removed from the bypass list.")
                return

            # Fetch the updated bypassed users list after removal
            
            await constants.fetch_bypassed_users()
            
            await ctx.send(f"<:whitecheck:1285350764595773451> {user.mention} has been removed from the bypass list.")
            
        except Exception as e:
            error_id = str(uuid.uuid4())
            await send_error_embed(interaction, e, error_id)
    


    # This is a custom sync command cause JSK sync is broken, this will sync the commands with Discord
    # guilds accross the platform that uses the bot.


    @commands.hybrid_command(name="sync", description="Sync commands to the guild or globally.")
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx: commands.Context):
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=PermissionDeniedEmbed())
            return
        
        synced = await self.merx.tree.sync()
        await ctx.send(f"<:whitecheck:1285350764595773451> Synced {len(synced)} commands. The new commands will be slash commands as well.")



    @add_owner.error
    async def add_owner_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=PermissionDeniedEmbed())
            
            
            
    @remove_owner.error
    async def remove_owner_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=PermissionDeniedEmbed())
        
        
        
    # This handles the permission denied and error embeds. It also generates
    # the UUID for the error embed.

    async def handle_permission_denied(self, ctx):
        embed = PermissionDeniedEmbed()
        await ctx.send(embed=embed)


    async def handle_error(self, ctx, error):
        error_id = str(uuid.uuid4())
        if isinstance(ctx, discord.Interaction):
            await send_error_embed(ctx, error, error_id)
        else:
            await ctx.send(embed=ErrorEmbed(error=error, error_id=error_id))



    # These are the cog error handlers they determine how the error is sent.

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.handle_error(ctx, error.original if isinstance(error, commands.CommandInvokeError) else error)


    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        await self.handle_error(interaction, error)


async def setup(merx):
    await merx.add_cog(AdminCommandsCog(merx))