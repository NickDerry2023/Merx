import discord
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import PrefixEmbed, PrefixSuccessEmbed

constants = MerxConstants()

class ChangePrefixCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
    

    
    @commands.hybrid_command(description="Change the prefix of the bot in your server.", with_app_command=True, extras={"category": "General"})
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str = None):
        
        
        mongo_db = await constants.mongo_setup()


        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return
        

        prefixes_collection = mongo_db['prefixes']
        

        if prefix is None:
            
            
            # Fetch the current prefix if no new prefix is provided
            
            current_prefix_doc = await prefixes_collection.find_one({"guild_id": str(ctx.guild.id)})
            current_prefix = current_prefix_doc.get("prefix", "!")
            embed = PrefixEmbed(current_prefix)
            await ctx.send(embed=embed)
            
            
        else:
            
            
            # Update the prefix if the user provides a new one
            
            result = await prefixes_collection.update_one(
                {"guild_id": str(ctx.guild.id)},
                {"$set": {"prefix": prefix}},
                upsert=True
            )
            

            embed = PrefixSuccessEmbed(prefix)
            await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(ChangePrefixCommandCog(merx))