import discord
from discord.ext import commands

class ChannelCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    # This allows the creation of a catagory.

    @commands.hybrid_command(description="Create a new channel or category.", with_app_command=True, extras={"category": "Administration"})
    async def add(self, ctx, name: str, type: str = "channel", category: discord.CategoryChannel = None):
        
        
        # Checks to see if its a catagory being made.
        
        if type.lower() == "category":
            category = await ctx.guild.create_category(name)
            await ctx.send(f"<:whitecheck:1285350764595773451> Category '{category.name}' created successfully!")
            
        
        # Checks to see if its a channel being made.
            
        elif type.lower() == "channel":
            if category:
                channel = await category.create_text_channel(name)
                await ctx.send(f"<:whitecheck:1285350764595773451> Channel '{channel.name}' created in category '{category.name}'!")
                
                
            else:
                channel = await ctx.guild.create_text_channel(name)
                await ctx.send(f"<:whitecheck:1285350764595773451> Channel '{channel.name}' created successfully!")
                
                
        else:
            await ctx.send("Please specify either 'category' or 'channel' as the type.")



    # This is the delete operation to delete channels or catagory.

    @commands.hybrid_command(description="Delete a channel or category.", with_app_command=True, extras={"category": "Administration"})
    async def delete(self, ctx, target: discord.abc.GuildChannel):


        await target.delete()
        await ctx.send(f"<:whitecheck:1285350764595773451> {target.name} has been deleted successfully.")


    # This allows the moving of the channel.

    @commands.hybrid_command(description="Move a channel to another category.", with_app_command=True, extras={"category": "Administration"})
    async def move(self, ctx, channel: discord.abc.GuildChannel, new_category: discord.CategoryChannel):


        await channel.edit(category=new_category)
        await ctx.send(f"<:whitecheck:1285350764595773451> Channel '{channel.name}' moved to category '{new_category.name}'.")



async def setup(merx):
    await merx.add_cog(ChannelCommandCog(merx))
