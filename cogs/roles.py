import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.embeds import RoleSuccessEmbed, ErrorEmbed
from cogs.utils.errors import send_error_embed

class RolesCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx



    @commands.hybrid_command(description="Allows server administrators to delete a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx: commands.Context, role: discord.Role):
        
        
        try:
            await role.delete(reason=f"Deleted by {ctx.author}")
            embed = RoleSuccessEmbed(title="Role Deleted", description=f"<:whitecheck:1285350764595773451> Role {role.name} has been deleted.")
            await ctx.send(embed=embed)
            

        except discord.Forbidden:
            embed = ErrorEmbed(title="Permission Denied", description="<:xmark:1285350796841582612> I don't have permission to delete this role.")
            await ctx.send(embed=embed)
            

        except discord.HTTPException:
            embed = ErrorEmbed(title="Error", description="<:xmark:1285350796841582612> An error occurred while trying to delete the role.")
            await ctx.send(embed=embed)



    @commands.hybrid_command(description="Allows server administrators to add a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, *, role_name: str):
        
        
        guild = ctx.guild
        
        
        try:
            new_role = await guild.create_role(name=role_name, reason=f"Created by {ctx.author}")
            embed = RoleSuccessEmbed(title="Role Created", description=f"<:whitecheck:1285350764595773451> Role {new_role.name} has been created.")
            await ctx.send(embed=embed)


        except discord.Forbidden:
            embed = ErrorEmbed(title="Permission Denied", description="<:xmark:1285350796841582612> I don't have permission to create roles.")
            await ctx.send(embed=embed)


        except discord.HTTPException:
            embed = ErrorEmbed(title="Error", description="<:xmark:1285350796841582612> An error occurred while trying to create the role.")
            await ctx.send(embed=embed)



    @commands.hybrid_command(description="Allows server administrators to assign a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def assignrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        
        
        try:
            await member.add_roles(role, reason=f"Assigned by {ctx.author}")
            embed = RoleSuccessEmbed(title="Role Assigned", description=f"<:whitecheck:1285350764595773451> Role {role.name} has been assigned to {member.mention}.")
            await ctx.send(embed=embed)


        except discord.Forbidden:
            embed = ErrorEmbed(title="Permission Denied", description="<:xmark:1285350796841582612> I don't have permission to assign this role.")
            await ctx.send(embed=embed)


        except discord.HTTPException:
            embed = ErrorEmbed(title="Error", description="<:xmark:1285350796841582612> An error occurred while trying to assign the role.")
            await ctx.send(embed=embed)



    @commands.hybrid_command(description="Allows server administrators to unassign a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def unassignrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        
        
        try:
            await member.remove_roles(role, reason=f"Unassigned by {ctx.author}")
            embed = RoleSuccessEmbed(title="Role Unassigned", description=f"<:whitecheck:1285350764595773451> Role {role.name} has been removed from {member.mention}.")
            await ctx.send(embed=embed)
            

        except discord.Forbidden:
            embed = ErrorEmbed(title="Permission Denied", description="<:xmark:1285350796841582612> I don't have permission to remove this role.")
            await ctx.send(embed=embed)
            

        except discord.HTTPException:
            embed = ErrorEmbed(title="Error", description="<:xmark:1285350796841582612> An error occurred while trying to remove the role.")
            await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(RolesCommandsCog(merx))
