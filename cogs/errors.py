import discord
from discord.ext import commands
from zuid import ZUID
from cogs.utils.embeds import MissingArgsEmbed, BadArgumentEmbed, ForbiddenEmbed, MissingPermissionsEmbed, UserErrorEmbed, DeveloperErrorEmbed


class OnCommandError(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        
        

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        
        
        error_id = ZUID(prefix="error_", length=10)
        error_id = error_id()
        
        
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed = MissingArgsEmbed(error.param.name)
            return await ctx.send(embed=embed)



        elif isinstance(error, commands.BadArgument):
            embed = BadArgumentEmbed()
            return await ctx.send(embed=embed)



        elif isinstance(error, discord.Forbidden):
            embed = ForbiddenEmbed()
            return await ctx.send(embed=embed)



        elif isinstance(error, commands.MissingPermissions):
            embed = MissingPermissionsEmbed()
            return await ctx.send(embed=embed)



        else:
            user_embed = UserErrorEmbed(error_id)
            await ctx.send(embed=user_embed)

            dev_embed = DeveloperErrorEmbed(error, ctx, error_id)
            guild = self.merx.get_guild(1285107028892717118)
            if not guild:
                guild = self.merx.get_guild(1285107028892717118)
            channel = discord.utils.get(guild.channels, name='errors')
            await channel.send(embed=dev_embed)
        
        

async def setup(merx):
    await merx.add_cog(OnCommandError(merx))