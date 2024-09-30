import discord
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import PermissionDeniedEmbed

constants = MerxConstants()

class ChangePrefixCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
    

    
    @commands.hybrid_command(description="Change the prefix of the bot in your server.", with_app_command=True, extras={"category": "General"})
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str):


        mongo_db = await constants.mongo_setup()


        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return


        prefixes_collection = mongo_db['prefixes']


        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send(embed=PermissionDeniedEmbed())
            return


        result = await prefixes_collection.update_one(
            {"guild_id": str(ctx.guild.id)},
            {"$set": {"prefix": prefix}},
            upsert=True
        )


        await ctx.send(f"Prefix successfully changed to {prefix}")



async def setup(merx):
    await merx.add_cog(ChangePrefixCommandCog(merx))