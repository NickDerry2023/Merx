import discord
from discord import Embed
from discord.ext import commands
from cogs.utils.constants import MerxConstants


constants = MerxConstants()


class EnlargeCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
    

    
    @commands.hybrid_command(description="Enlarges a provided emoji.", with_app_command=True, extras={"category": "General"})
    async def enlarge(self, ctx, emoji: discord.Emoji):


        if emoji == None:
            embed = Embed(
                title="",
                description="<:xmark:1285350796841582612> I could not find that emoji."
            )
            await ctx.reply(embed=embed)
            return
        

        emoji_url = emoji.url


        embed = Embed(color=constants.merx_embed_color_setup()).set_thumbnail(url=emoji_url)

        
        await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(EnlargeCommandCog(merx))