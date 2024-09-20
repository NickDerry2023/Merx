import discord
from discord.ext import commands
from discord import app_commands

class RolesCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx



    # Hybrid command to delete a role
    @commands.hybrid_command(description="Allows server administrators to delete a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx: commands.Context, role: discord.Role):
        
        
        try:
            await role.delete(reason=f"Deleted by {ctx.author}")
            await ctx.send(f"<:whitecheck:1285350764595773451> Role {role.name} has been deleted.")
            
            
        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I don't have permission to delete this role.")
            
            
        except discord.HTTPException:
            await ctx.send("<:xmark:1285350796841582612> An error occurred while trying to delete the role.")



    # Hybrid command to create a role
    @commands.hybrid_command(description="Allows server administrators to add a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, *, role_name: str):
        
        
        guild = ctx.guild
        
        
        try:
            new_role = await guild.create_role(name=role_name, reason=f"Created by {ctx.author}")
            await ctx.send(f"<:whitecheck:1285350764595773451> Role {new_role.name} has been created.")
            
            
        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I don't have permission to create roles.")
            
            
        except discord.HTTPException:
            await ctx.send("<:xmark:1285350796841582612> An error occurred while trying to create the role.")



    # Hybrid command to assign a role to a user
    
    @commands.hybrid_command(description="Allows server administrators to assign a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def assignrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):


        try:
            await member.add_roles(role, reason=f"Assigned by {ctx.author}")
            await ctx.send(f"<:whitecheck:1285350764595773451> Role {role.name} has been assigned to {member.mention}.")
            
            
        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I don't have permission to assign this role.")
            
            
        except discord.HTTPException:
            await ctx.send("<:xmark:1285350796841582612> An error occurred while trying to assign the role.")



    # Hybrid command to unassign (remove) a role from a user
    
    @commands.hybrid_command(description="Allows server administrators to unassign a role.", with_app_command=True, extras={"category": "Administration"})
    @commands.has_permissions(manage_roles=True)
    async def unassignrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):

        
        try:
            await member.remove_roles(role, reason=f"Unassigned by {ctx.author}")
            await ctx.send(f"<:whitecheck:1285350764595773451> Role {role.name} has been removed from {member.mention}.")
            
            
        except discord.Forbidden:
            await ctx.send("<:xmark:1285350796841582612> I don't have permission to remove this role.")
            
            
        except discord.HTTPException:
            await ctx.send("<:xmark:1285350796841582612> An error occurred while trying to remove the role.")



async def setup(merx):
    await merx.add_cog(RolesCommandsCog(merx))
