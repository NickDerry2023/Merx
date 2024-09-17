import discord
from discord.ext import commands
from cogs.utils.errors import send_error_embed
from cogs.utils.embeds import DebugEmbed, PermissionDeniedEmbed
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
            await ctx.send(f"<:xmark:1285350796841582612> Hmmm... something did not complete correctly: {str(e)}")



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
            await ctx.send(f"<:xmark:1285350796841582612> Hmmm... something did not complete correctly: {str(e)}")
    


    @add_owner.error
    async def add_owner_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("<:xmark:1285350796841582612> You do not have permission to use this command.")
            
            
            
    @remove_owner.error
    async def remove_owner_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("<:xmark:1285350796841582612> You do not have permission to use this command.")
        

async def setup(merx):
    await merx.add_cog(AdminCommandsCog(merx))