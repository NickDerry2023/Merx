import discord
from discord.ext import commands
from cogs.utils.embeds import ChannelSuccessEmbed, ErrorEmbed
from cogs.utils.errors import send_error_embed

class ChannelCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    # This allows the creation of a catagory.

    @commands.hybrid_command(description="Create a new channel or category.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, name: str, type: str = "channel", category: discord.CategoryChannel = None):
        
        
        if type.lower() == "category":
            category = await ctx.guild.create_category(name)
            embed = ChannelSuccessEmbed(title="Category Created", description=f"<:whitecheck:1285350764595773451> Category '{category.name}' created successfully!")
            await ctx.send(embed=embed)
            
            
        elif type.lower() == "channel":
            
            
            if category:
                channel = await category.create_text_channel(name)
                embed = ChannelSuccessEmbed(title="Channel Created", description=f"<:whitecheck:1285350764595773451> Channel '{channel.name}' created in category '{category.name}'!")
                await ctx.send(embed=embed)
                
                
            else:
                channel = await ctx.guild.create_text_channel(name)
                embed = ChannelSuccessEmbed(title="Channel Created", description=f"<:whitecheck:1285350764595773451> Channel '{channel.name}' created successfully!")
                await ctx.send(embed=embed)
                
                
        else:
            await ctx.send("<:xmark:1285350796841582612> Please specify either 'category' or 'channel' as the type.")



    @commands.hybrid_command(description="Delete a channel or category.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, target: discord.abc.GuildChannel):
        
        
        await target.delete()
        embed = ChannelSuccessEmbed(title="Deleted Target", description=f"<:whitecheck:1285350764595773451> {target.name} has been deleted successfully.")
        await ctx.send(embed=embed)



    @commands.hybrid_command(description="Move a channel to another category.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(administrator=True)
    async def move(self, ctx, channel: discord.abc.GuildChannel, new_category: discord.CategoryChannel):
        
        
        await channel.edit(category=new_category)
        embed = ChannelSuccessEmbed(title="Channel Moved", description=f"<:whitecheck:1285350764595773451> Channel '{channel.name}' moved to category '{new_category.name}'.")
        await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(ChannelCommandCog(merx))
