import discord
from discord.ext import commands
from cogs.utils.constants import MerxConstants

constants = MerxConstants()

class AvatarCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    # This is the avatar command that will allow users to run /av or prefix!av to see their own
    # or another users avatar in an embed state.

    @commands.hybrid_command(name="av", description="Displays the avatar of a user. If no user is mentioned, shows your avatar.", with_app_command=True, extras={"category": "General"})
    async def av(self, ctx, user: discord.User = None):
        try:
            
            if user is None:
                user = ctx.author
            
            
            embed = discord.Embed(
                title=f"{user}'s Avatar",
                color=constants.merx_embed_color_setup()
            )
            
            
            # Send the actual embed with a footer.
            
            embed.set_image(url=user.avatar.url)
            embed.set_footer(text=f"Requested by {ctx.author}")


            await ctx.send(embed=embed)


        except Exception as e:
            error_id = shortuuid.ShortUUID().random(length=8)
            await send_error_embed(ctx, e, error_id)



async def setup(merx):
    await merx.add_cog(AvatarCommandCog(merx))
