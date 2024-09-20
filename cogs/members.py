import discord
import math
from cogs.utils.constants import MerxConstants
from discord.ext import commands


constants = MerxConstants()


class MembersCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
    
    
    
    @commands.hybrid_command(description="Lists the amount of members a role is assigned to. You can pass specific_role to run the command.", with_app_command=True, extras={"category": "General"})
    async def members(self, ctx, *, specific_role: discord.Role):

        if not specific_role:
            await ctx.send("Role not found.")
            return
        

        await ctx.guild.chunk()
        members_with_role = [member for member in ctx.guild.members if specific_role in member.roles]
        
        
        if not members_with_role:
            await ctx.send(f"No members have the role {specific_role.name}.")
            return
        
        
        embed = discord.Embed(
            title=f"Members with the role `{specific_role.name}`",
            description=f"{len(members_with_role)} members have this role",
            color=constants.merx_embed_color_setup()
        )

        
        member_list = "\n".join([f"**{member.display_name}** ({member.id})" for member in members_with_role])


        embed.add_field(
            name="",
            value=member_list,
            inline=False
        )

        
        await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(MembersCommandsCog(merx))
