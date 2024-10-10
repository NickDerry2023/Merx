import discord
from discord.ext import commands
from utils.constants import MerxConstants
 

constants = MerxConstants()

class AvatarCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    # This is the avatar command that will allow users to run /av or prefix!av to see their own
    # or another users avatar in an embed state.

    @commands.hybrid_command(name="av", description="Displays the avatar of a user. If no user is mentioned, shows your avatar.", with_app_command=True, extras={"category": "General"})
    async def av(self, ctx, user: discord.User = None):

            
        if user is None:
            user = ctx.author
        
        
        embed = discord.Embed(
            title=f"{user}'s Avatar",
            color=constants.merx_embed_color_setup()
        )
        
        
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")


        await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(AvatarCommandCog(merx))
