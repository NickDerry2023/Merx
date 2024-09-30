import discord
import asyncio
import uuid
import shortuuid
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import ErrorEmbed, PermissionDeniedEmbed, UserInformationEmbed, SuccessEmbed
from cogs.utils.errors import send_error_embed


constants = MerxConstants()


class ModLogsCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()



    # This is the logic to get mod logs from the MongoDB database. This gets the modlogs from the diffrent collections.

    async def getModLogsLogic(self, user_id):
        
        
        mongo_db = await self.constants.mongo_setup()
        
        
        if mongo_db is None:
            return None, "Failed to connect to the database."
        
        
        warn_collection = mongo_db["warns"]
        bans = mongo_db["bans"]
        blacklist_collection = mongo_db["blacklists"]


        warnings = await warn_collection.find({"warned_user_id": str(user_id)}).to_list(length=None)
        bans = await bans.find({"banned_user_id": str(user_id)}).to_list(length=None)
        blacklists = await blacklist_collection.find({"discord_id": str(user_id)}).to_list(length=None)
        
        
        logs = {
            "warnings": warnings,
            "bans": bans,
            "blacklists": blacklists
        }
        
        
        return logs, None
    
    
    
    # This is the logic to actually proccess the transfer of the modlogs.
    
    async def transferUpdateModLogsLogic(self, user_id, logs):
        
        
        mongo_db = await self.constants.mongo_db()
        
        
        if mongo_db is None:
            return "Failed to connect to the database"
        
        
        warn_collection = mongo_db["warns"]
        bans = mongo_db["bans"]
        blacklist_collection = mongo_db["blacklists"]
        
        
        if logs['warnings']:
            for warn in logs['warnings']:
                
                
                await warn_collection.update_one({"_id": warn["_id"]}, {"$set": {"warned_user_id": str(user_id)}})
                
                
        if logs['bans']:
            for ban in logs['bans']:
                
                
                await bans.update_one({"_id": ban["_id"]}, {"$set": {"banned_user_id": str(user_id)}})
                
                
        if logs['blacklists']:
            for blacklist in logs['blacklists']:
                
                
                await blacklist_collection.update_one({"_id": blacklist["_id"]}, {"$set": {"discord_id": str(user_id)}})



    # This is the logic to proccess the deletion of a modlog.

    async def deleteModLogsLogic(self, user_id):
        
        mongo_db = await self.constants.mongo_db()
        
        
        if mongo_db is None:
            return "Failed to connect to the database"
        
        
        warn_collection = mongo_db["warns"]
        bans = mongo_db["bans"]
        blacklist_collection = mongo_db["blacklists"]
        
        
        return None



    # This is the set of commands that will be used via Discord to actually carry out the transfer and clearing of modlogs.

    @commands.hybrid_command(description="Allows users to transfer modlogs from one user to another.", with_app_command=True, extras={"category": "Moderation"})
    async def transfermodlogs(self, ctx, member_from: discord.Member = None, member_to: discord.Member = None):
        
        
        if not member_from or not member_to:
            await ctx.send(embed=ErrorEmbed(description="You must specify both the source and destination members."))
            return
        
        
        logs, error = await self.getModLogsLogic(member_from.id)
        if error:
            await ctx.send(embed=ErrorEmbed(description=error))
            return


        if not logs or (not logs['warnings'] and not logs['bans'] and not logs['blacklists']):
            await ctx.send(embed=ErrorEmbed(description=f"No mod logs found for {member_from.display_name}."))
            return


        error = await self.transferUpdateModLogsLogic(member_to.id, logs)
        if error:
            await ctx.send(embed=ErrorEmbed(description=error))
            return
        
        
        await self.delete_modlogs(member_from.id)

        await ctx.send(embed=SuccessEmbed(description=f"Mod logs have been transferred from {member_from.display_name} to {member_to.display_name}."))

        
        
    # Command to clear modlogs.
    
    @commands.hybrid_command(description="Allows users to delete modlogs from a user.", with_app_command=True, extras={"category": "Moderation"})
    async def clearmodlogs(self, ctx, member: discord.Member = None):
        
        
        if not member:
            await ctx.send(embed=ErrorEmbed(description="You must specify a member to clear mod logs for."))
            return


        logs, error = await self.getModLogsLogic(member.id)
        if error:
            await ctx.send(embed=ErrorEmbed(description=error))
            return
        

        if not logs or (not logs['warnings'] and not logs['bans'] and not logs['blacklists']):
            await ctx.send(embed=ErrorEmbed(description=f"No mod logs found for {member.display_name}."))
            return



        error = await self.deleteModLogsLogic(member.id)
        if error:
            await ctx.send(embed=ErrorEmbed(description=error))
            return


        await ctx.send(embed=SuccessEmbed(description=f"All mod logs for {member.display_name} have been cleared."))



async def setup(merx):
    await merx.add_cog(ModLogsCommandCog(merx))