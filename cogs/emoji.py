import discord
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import EmojiFindEmbed

constants = MerxConstants()

class EmojiCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
    


    @commands.hybrid_command(description="Finds and shows info about a emoji", with_app_command=True, extras={"category": "General"})
    async def emoji_find(self, ctx, emoji: discord.Emoji):


        if emoji.name == None:
            await ctx.send("<:xmark:1285350796841582612> I couldn't find that emoji.")
            return
        

        await ctx.send(embed=EmojiFindEmbed(emoji).create_embed())
    


    @commands.hybrid_command(description="Shows all the emojis in the server.", with_app_command=True, extras={"category": "General"})
    async def emojis(self, ctx: commands.Context):
        emojis = "".join(f"{emoji}" for emoji in ctx.guild.emojis)


        embed = discord.Embed(
            description=emojis,
            color=constants.merx_embed_color_setup()
        )


        embed.set_author(name=f"{ctx.guild.name} emojis", icon_url=ctx.guild.icon.url)


        await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(EmojiCommandsCog(merx))