import discord
from utils.constants import MerxConstants
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
        
        
        
    @commands.hybrid_command(description="This lists the servers members", with_app_command=True, extras={"category": "General"})
    async def membercount(self, ctx: commands.Context):
        guild = ctx.guild

        if not guild.chunked:
            await guild.chunk()

        member_count = guild.member_count
        server_boosts = guild.premium_subscription_count

        # online_members = []
        # for member in guild.members:
        #     print(member.status)
        # return

        # online_members = len([member for member in guild.members if member.status != discord.Status.offline])
        server_icon_url = guild.icon.url if guild.icon else None
        server_name = guild.name
        
        embed = discord.Embed(
            description="",
            color=constants.merx_embed_color_setup()
        )
        
        if server_icon_url:
            embed.set_author(name=server_name, icon_url=server_icon_url)

        embed.add_field(
            name="Member Count",
            value=member_count,
            inline=True
        )
        
        # embed.add_field(
        #     name="Online Members",
        #     value=online_members,
        #     inline=True
        # )
        
        embed.add_field(
            name="Server Boosts",
            value=server_boosts,
            inline=True
        )
        
        await ctx.send(embed=embed)



async def setup(merx):
    await merx.add_cog(MembersCommandsCog(merx))
