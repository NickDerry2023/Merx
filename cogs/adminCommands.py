import discord
import asyncio
import uuid
import shortuuid
from discord.ext import commands
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
        
        
        # Check if the user running the command has the required role
        
        merx_team_role = discord.utils.get(ctx.author.roles, id=1285107029093912637)
        developer_role = discord.utils.get(ctx.author.roles, id=1285107029093912638)
        
        if not merx_team_role or developer_role:
            await ctx.send("<:xmark:1285350796841582612> You do not have the required role to use this command.")
            return
        
        
        # Displays debugging information.
        # Check if the user has administrator permissions
        
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=PermissionDeniedEmbed())
            return


        # Send the embed with debugging information
        
        await ctx.send(embed=DebugEmbed(self.merx, ctx))
        
       
        
    # This command will add users into blacklist_bypass collection so they can run commands like JSK
    # and blacklist_guild or blacklist_user.
        
    @commands.hybrid_command(name="addowner", description="Add a user to the bypassed list.", with_app_command=True, extras={"category": "Debugging"})
    @commands.has_permissions(administrator=True)
    async def addowner(self, ctx: commands.Context, user: discord.User):
        
        
        # Check if the command is run in the correct guild
        
        if ctx.guild.id != 1285107028892717118:
            await ctx.send("<:xmark:1285350796841582612> This command can only be used in the Merx server.")
            return
        

        # Check if the user running the command has the required role
        
        role = discord.utils.get(ctx.author.roles, id=1285107029093912637)
        
        if not role:
            await ctx.send("<:xmark:1285350796841582612> You do not have the required role to use this command.")
            return
        
        
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
    
    @commands.hybrid_command(name="removeowner", description="Remove a user from the bypassed list.", with_app_command=True, extras={"category": "Debugging"})
    @commands.has_permissions(administrator=True)
    async def removeowner(self, ctx: commands.Context, user: discord.User):
        
        
        # Check if the command is run in the correct guild
        
        if ctx.guild.id != 1285107028892717118:
            await ctx.send("<:xmark:1285350796841582612> This command can only be used in the Merx server.")
            return
        

        # Check if the user running the command has the required role
        
        role = discord.utils.get(ctx.author.roles, id=1285107029093912637)
        
        if not role:
            await ctx.send("<:xmark:1285350796841582612> You do not have the required role to use this command.")
            return
        
        
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
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(interaction, e, error_id)
    


    # This is a custom sync command cause JSK sync is broken, this will sync the commands with Discord
    # guilds accross the platform that uses the bot.


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx: commands.Context):
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=PermissionDeniedEmbed())
            return
        
        synced = await self.merx.tree.sync()
        await ctx.send(f"<:whitecheck:1285350764595773451> Synced {len(synced)} commands. The new commands will be slash commands as well.")



    @addowner.error
    async def add_owner_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=PermissionDeniedEmbed())
            
            
            
    @removeowner.error
    async def remove_owner_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=PermissionDeniedEmbed())
        
        
    # Checks if the user is in the blacklist bypass also known as
    # bot owners collection so that only we can blacklist users.
    

    async def is_bypassed_user(self, user_id):
        collection = constants.mongo_db["blacklist_bypass"]
        return await collection.find_one({"discord_id": user_id})        



    # This is the set of commands to unblacklist a user from the bot. This follows the same set of logic as
    # blacklisting the user but in the opposit order.

    @commands.hybrid_command(name="unblacklist", description="Remove a user or guild from the blacklist.", with_app_command=True, extras={"category": "Administration"})
    async def unblacklist(self, ctx: commands.Context, id: str, entity_type: str, reason: str = "No reason provided."):
        
        
        # Check if the command is run in the correct guild
        
        if ctx.guild.id != 1285107028892717118:
            await ctx.send("<:xmark:1285350796841582612> This command can only be used in the Merx server.")
            return
        

        # Check if the user running the command has the required role
        
        role = discord.utils.get(ctx.author.roles, id=1285107029093912637)
        
        if not role:
            await ctx.send("<:xmark:1285350796841582612> You do not have the required role to use this command.")
            return
        
        
        # Checks to see if the user is bypassed and bot owner. Then it checks to see if you pass
        # the righr parmeter.
        
        bypassed = await self.is_bypassed_user(ctx.author.id)
        
        
        if not bypassed:
            await self.send_message(ctx, embed=PermissionDeniedEmbed())
            return


        if entity_type not in ["user", "guild"]:
            await self.send_message(ctx, "Invalid entity type. Please specify either `user` or `guild`.")
            return


        collection = constants.mongo_db["blacklists"]
        case_number = f"Case #{str(uuid.uuid4().int)[:4]}"


        # This checks to see if its a user that was passed and proceedes to do the blacklist
        # logic for a user and not a guild.

        if entity_type == "user":
            
            
            try:
                user = await self.merx.fetch_user(int(id))
                result = await collection.delete_one({"discord_id": user.id, "type": "user"})
                if result.deleted_count == 0:
                    await self.send_message(ctx, f"<:xmark:1285350796841582612> {user.mention} is not blacklisted.")
                    return


                try:
                    await user.send(f"You have been unblacklisted. **Reason:** {reason}")
                    
                    
                except discord.Forbidden:
                    await self.send_message(ctx, f"Could not DM {user.mention}, but they were successfully unblacklisted.")

                await self.send_message(ctx, f"<:whitecheck:1285350764595773451> **{case_number} - {user.mention}** has been unblacklisted.")
            
            
            except discord.NotFound:
                await self.send_message(ctx, f"<:xmark:1285350796841582612> User with ID `{id}` not found.")
            
            
            except Exception as e:
                await self.send_message(ctx, f"Error unblacklisting user: {e}")
                return


        # This checks if its a guild that was passed and proceeds to blacklist the guild.
        # note that this is overpowered and you can blacklist guilds that dont even use
        # Merx Bot. This could be used as an abuse of power so use it wisely. Don't be stupid.

        elif entity_type == "guild":
            guild_id = int(id)
            result = await collection.delete_one({"discord_id": guild_id, "type": "guild"})
            
            
            if result.deleted_count == 0:
                await self.send_message(ctx, f"<:xmark:1285350796841582612> Guild with ID `{id}` is not blacklisted.")
                return


            await self.send_message(ctx, f"<:whitecheck:1285350764595773451> **{case_number} - Guild ID {id}** has been unblacklisted.")



    async def send_message(self, ctx, content=None, embed=None):
        
        if isinstance(ctx, discord.Interaction):
            
            if ctx.response.is_done():
                await ctx.followup.send(content=content, embed=embed)
                
            else:
                await ctx.response.send_message(content=content, embed=embed)
                
                
        else:
            await ctx.send(content=content, embed=embed)



    # Error handling for unblacklist command
    
    @unblacklist.error
    async def unblacklist_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await self.send_message(ctx, embed=PermissionDeniedEmbed())
        else:
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(ctx, error, error_id)

        
        
    # This set of commands allows server administrators to blacklist the bot and prevent users
    # from runing commands.

    @commands.hybrid_command(name="blacklist", description="Blacklist a user or guild.", with_app_command=True, extras={"category": "Administration"})
    async def blacklist(self, ctx: commands.Context, id: str, entity_type: str):
        
        
        # Check if the command is run in the correct guild
        
        if ctx.guild.id != 1285107028892717118:
            await ctx.send("<:xmark:1285350796841582612> This command can only be used in the Merx server.")
            return
        

        # Check if the user running the command has the required role
        
        role = discord.utils.get(ctx.author.roles, id=1285107029093912637)
        
        if not role:
            await ctx.send("<:xmark:1285350796841582612> You do not have the required role to use this command.")
            return
        
        
        # Checks to see if the user is bypassed and bot owner. Then it checks to see if you pass
        # the righr parmeter.
        
        bypassed = await self.is_bypassed_user(ctx.author.id)
        
        
        if not bypassed:
            await self.send_message(ctx, embed=PermissionDeniedEmbed())
            return

        
        if entity_type not in ["user", "guild"]:
            await self.send_message(ctx, "<:xmark:1285350796841582612> Invalid entity type. Please specify either `user` or `guild`.")
            return

        
        collection = constants.mongo_db["blacklists"]
        case_number = f"Case #{str(uuid.uuid4().int)[:4]}"

        
        # This checks to see if its a user that was passed and proceedes to do the blacklist
        # logic for a user and not a guild.
        
        if entity_type == "user":
            
            
            try:
                user = await self.merx.fetch_user(int(id))
                if await collection.find_one({"discord_id": user.id, "type": "user"}):
                    await self.send_message(ctx, f"<:xmark:1285350796841582612> {user.mention} is already blacklisted.")
                    return

                await collection.insert_one({"discord_id": user.id, "type": "user", "case_number": case_number})
                await self.send_message(ctx, f"<:whitecheck:1285350764595773451> **{case_number} - {user.mention}** has been blacklisted.")
            
            
            except discord.NotFound:
                await self.send_message(ctx, f"<:xmark:1285350796841582612> User with ID `{id}` not found.")
            
            
            except Exception as e:
                await self.send_message(ctx, f"Error blacklisting user: {e}")
                return


        # This checks if its a guild that was passed and proceeds to blacklist the guild.
        # note that this is overpowered and you can blacklist guilds that dont even use
        # Merx Bot. This could be used as an abuse of power so use it wisely. Don't be stupid.

        elif entity_type == "guild":
            
            guild_id = int(id)
            
            
            if await collection.find_one({"discord_id": guild_id, "type": "guild"}):
                await self.send_message(ctx, f"<:xmark:1285350796841582612> Guild with ID `{id}` is already blacklisted.")
                return


            await collection.insert_one({"discord_id": guild_id, "type": "guild", "case_number": case_number})
            await self.send_message(ctx, f"<:whitecheck:1285350764595773451> **{case_number} - Guild ID {id}** has been blacklisted.")




    # This is the logic to send the message depending how the command is run
    # either slash commands or prefix, we do it this way so that the command
    # works regarless of how its run, this makes it easier on the user.

    async def send_message(self, ctx, content=None, embed=None):


        if isinstance(ctx, discord.Interaction):
            
            if ctx.response.is_done():
                await ctx.followup.send(content=content, embed=embed)
            else:
                await ctx.response.send_message(content=content, embed=embed)
                
                
        else:
            await ctx.send(content=content, embed=embed)



    # This is the error handling for the blacklist logic incase something goes wrong, like
    # incorrect permissions.
    
    @blacklist.error
    async def blacklist_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await self.send_message(ctx, embed=PermissionDeniedEmbed())
        else:
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(ctx, error, error_id)   
    
        
        

async def setup(merx):
    await merx.add_cog(AdminCommandsCog(merx))