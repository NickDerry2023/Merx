import discord
from discord.ext import commands
from utils.embeds import RoleSuccessEmbed, RolesInformationEmbed
 

class RolesCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx



    @commands.hybrid_command(description="Allows server administrators to delete a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx: commands.Context, role: discord.Role):


        await role.delete(reason=f"Deleted by {ctx.author}")
        embed = RoleSuccessEmbed(title="Role Deleted", description=f"<:whitecheck:1285350764595773451> Role {role.name} has been deleted.")
        await ctx.send(embed=embed)



    @commands.hybrid_command(description="Allows server administrators to add a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, *, role_name: str):
        
        
        guild = ctx.guild
        

        new_role = await guild.create_role(name=role_name, reason=f"Created by {ctx.author}")
        embed = RoleSuccessEmbed(title="Role Created", description=f"<:whitecheck:1285350764595773451> Role {new_role.name} has been created.")
        await ctx.send(embed=embed)



    @commands.hybrid_command(description="Allows server administrators to assign a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def assignrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        
        
        await member.add_roles(role, reason=f"Assigned by {ctx.author}")
        embed = RoleSuccessEmbed(title="Role Assigned", description=f"<:whitecheck:1285350764595773451> Role {role.name} has been assigned to {member.mention}.")
        await ctx.send(embed=embed)



    @commands.hybrid_command(description="Allows server administrators to unassign a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def unassignrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        

        await member.remove_roles(role, reason=f"Unassigned by {ctx.author}")
        embed = RoleSuccessEmbed(title="Role Unassigned", description=f"<:whitecheck:1285350764595773451> Role {role.name} has been removed from {member.mention}.")
        await ctx.send(embed=embed)
        
        
        
    @commands.hybrid_command(description="Shows information about a specific role.", with_app_command=True, extras={"category": "Setup"})
    async def roleinfo(self, target, role: discord.Role):
        embed = RolesInformationEmbed.create(role, target)

        if isinstance(target, discord.Interaction):
            await target.response.send_message(embed=embed)
        else:
            await target.send(embed=embed)
            


async def setup(merx):
    await merx.add_cog(RolesCommandsCog(merx))
