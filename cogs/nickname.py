import discord
import asyncio
import uuid
from discord.ext import commands
from cogs.utils.embeds import NicknameSuccessEmbed, ErrorEmbed, PermissionDeniedEmbed
from cogs.utils.errors import send_error_embed
from cogs.utils.constants import MerxConstants


constants = MerxConstants()


class NickCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    # This is the command that you can use to nickname users. You can enter the user you want to nickname
    # followed by the new name. To clear a nickname you can do m-nick @User followed by no new name.
    # You can also use User IDs instead of pinging the user.

    @commands.hybrid_command(description="Allows you to nickname a user in a server to whatever you want.", with_app_command=True, extras={"category": "General"})
    @commands.has_permissions(administrator=True)
    async def nick(self, ctx, member: discord.Member, *, nickname: str = None):


        previous_nickname = member.display_name


        try:
            
            await member.edit(nick=nickname if nickname else None)

            embed = NicknameSuccessEmbed(
                user=member,
                previous_name=previous_nickname,
                new_name=nickname if nickname else "Cleared"
            )
            
            await ctx.send(embed=embed)


        # Checks permissions and for common command errors.

        except discord.Forbidden:
            await self.handle_permission_denied(ctx)
            
            
        except (discord.HTTPException, discord.ext.commands.MemberNotFound) as e:
            await self.handle_error(ctx, e)
            

        except Exception as e:
            await self.handle_error(ctx, e)



    # This handles the permission denied and error embeds. It also generates
    # the UUID for the error embed.

    async def handle_permission_denied(self, ctx):
        embed = PermissionDeniedEmbed()
        await ctx.send(embed=embed)


    async def handle_error(self, ctx, error):
        error_id = str(uuid.uuid4())
        if isinstance(ctx, discord.Interaction):
            await send_error_embed(ctx, error, error_id)
        else:
            await ctx.send(embed=ErrorEmbed(error=error, error_id=error_id))



    # These are the cog error handlers they determine how the error is sent.

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.handle_error(ctx, error.original if isinstance(error, commands.CommandInvokeError) else error)


    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):
        await self.handle_error(interaction, error)



async def setup(merx):
    await merx.add_cog(NickCommandCog(merx))
