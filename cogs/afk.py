import discord
import shortuuid
from discord.ext import commands
from cogs.utils.embeds import SuccessEmbed, ErrorEmbed, PermissionDeniedEmbed, AfkEmbed
from cogs.utils.constants import MerxConstants
from cogs.utils.errors import send_error_embed

constants = MerxConstants()


class AfkCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        
        

    @commands.hybrid_command(name="afk", description="Set your AFK status with an optional reason.")
    async def afk(self, ctx, *, reason: str = "No reason provided."):
        
        
        mongo_db = await constants.mongo_setup()
        
        
        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return  
        
        
        afks_collection = mongo_db["afks"]
        
        
        await afks_collection.update_one(
            {"user_id": ctx.author.id},
            {"$set": {"user_id": ctx.author.id, "reason": reason}},
            upsert=True
        )
        
        
        await ctx.send(embed=SuccessEmbed(
            title="AFK Status Set",
            description=f"<:whitecheck:1285350764595773451> You are now AFK. Reason: {reason}"
        ))
        
        

    @commands.Cog.listener()
    async def on_message(self, message):
        
        
        if message.author.bot:
            return


        mongo_db = await constants.mongo_setup()
        
        
        if mongo_db is None:
            return
        
        
        afks_collection = mongo_db["afks"]


        if message.mentions:
            for user in message.mentions:
                afk_data = await afks_collection.find_one({"user_id": user.id})
                
                
                if afk_data:
                    await message.channel.send(embed=AfkEmbed(user, afk_data["reason"]))

            
            

    @commands.hybrid_command(name="back", description="Set your status back to online.")
    async def back(self, ctx):


        mongo_db = await constants.mongo_setup()
        
        
        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return
        
        
        afks_collection = mongo_db["afks"]

        afk_data = await afks_collection.find_one({"user_id": ctx.author.id})
        

        if afk_data:
            
            await afks_collection.delete_one({"user_id": ctx.author.id})
            
            
            await ctx.send(embed=SuccessEmbed(
                title="AFK Status Removed",
                description="<:whitecheck:1285350764595773451> You are now back online!"
            ))
            
            
        else:
            await ctx.send("You are not AFK.")



async def setup(merx):
    await merx.add_cog(AfkCommandCog(merx))
