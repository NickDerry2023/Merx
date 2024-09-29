import discord
import shortuuid
from discord.ext import commands
from cogs.utils.embeds import SuccessEmbed, ErrorEmbed, PermissionDeniedEmbed
from cogs.utils.constants import MerxConstants
from cogs.utils.errors import send_error_embed

constants = MerxConstants()


class AfkCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.afk_users = {}
        
        

    @commands.hybrid_command(name="afk", description="Set your AFK status with an optional reason.")
    async def afk(self, ctx, *, reason: str = "No reason provided."):


        self.afk_users[ctx.author.id] = reason
        
        
        await ctx.send(embed=SuccessEmbed(
            title="AFK Status Set",
            description=f"<:whitecheck:1285350764595773451> You are now AFK. Reason: {reason}"
        ))
        
        

    @commands.Cog.listener()
    async def on_message(self, message):
        
        
        if message.author.bot:
            return


        if message.author.id in self.afk_users:
            
            reason = self.afk_users[message.author.id]
            
            error_id = shortuuid.ShortUUID().random(length=8)
            
            await message.channel.send(embed=ErrorEmbed(error_id))


            del self.afk_users[message.author.id]
            
            

    @commands.hybrid_command(name="back", description="Set your status back to online.")
    async def back(self, ctx):


        if ctx.author.id in self.afk_users:
            
            del self.afk_users[ctx.author.id]
            
            await ctx.send(embed=SuccessEmbed(
                title="AFK Status Removed",
                description="<:whitecheck:1285350764595773451> You are now back online!"
            ))
            
            
        else:
            await ctx.send("You are not AFK.")



async def setup(merx):
    await merx.add_cog(AfkCommandCog(merx))
