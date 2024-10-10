import discord
from discord.ext import commands
from utils.embeds import SuccessEmbed, AfkEmbed
from utils.constants import MerxConstants, afks
import time
 
class AfkCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()
        

    @commands.hybrid_group(description="Set your AFK status with an optional reason.")
    async def afk(self, ctx: commands.Context):
        return
    
    @afk.group(name='mod', description="Group of a group")
    async def afk_mod(self, ctx: commands.Context):
        return
        
    @afk.command(name='set', description="Set yourself as AFK.", with_app_command=True)
    async def afk_set(self, ctx: commands.Context, *, message: str = "none"):
        afk_data = await afks.find_one({"user_id": ctx.author.id})
        
        if not afk_data:
            afk_doc = {
                'user_id': ctx.author.id,
                'guild_id': ctx.guild.id,
                'message': message,
                'timestamp': int(time.time())
            }
            await afks.insert_one(afk_doc)

            await ctx.author.edit(nick=f"[AFK] {ctx.author.global_name}")

            afk_doc_2 = {
                'user_id': ctx.author.id,
                'guild_id': ctx.guild.id
            }
            self.merx.afk_users.append(afk_doc_2)
            
            await ctx.send(embed=SuccessEmbed(
                title="AFK Status Set",
                description=f"<:whitecheck:1285350764595773451> You are now AFK."
            ))
        elif afk_data:
            await ctx.send("You are already on AFK!")

    @afk.command(name="return", description="Return from your AFK")
    async def afk_return(self, ctx: commands.Context):
        afk_data = await afks.find_one({"user_id": ctx.author.id})
        
        if afk_data:
            await afks.delete_one({"user_id": ctx.author.id})

            await ctx.author.edit(nick=None)

            for item in self.merx.afk_users:
                if item['user_id'] == ctx.author.id and item['guild_id'] == ctx.guild.id:
                    self.merx.afk_users.remove(item)
                    break

            await ctx.send(embed=SuccessEmbed(
                title="AFK Status Removed",
                description="<:whitecheck:1285350764595773451> You are now back online!"
            ))
        else:
            await ctx.send("You are not AFK.")
    
    @afk_mod.command(name='return', description="Force an AFK return", with_app_command=True)
    async def afk_return(self, ctx: commands.Context, member: discord.Member, *, reason: str = "None"):
        afk_data = await afks.find_one_and_delete({"user_id": ctx.author.id})
        
        if afk_data:
            await member.edit(nick=None)

            for item in self.merx.afk_users:
                if item['user_id'] == member.id and item['guild_id'] == ctx.guild.id:
                    self.merx.afk_users.remove(item)
                    break

            await ctx.send(f"**{member.name}**'s AFK has been ended!")
            await member.send(f"Your AFK has been ended in **{ctx.guild.name}** by **{ctx.author.mention}** for reason: {reason}")
        else:
            await ctx.send("I could not find an AFK for this person!")
    
    @afk_mod.command(name='list', description="List all AFK's in this server", with_app_command=True)
    async def afk_list(self, ctx: commands.Context):
        all_afks = afks.find({"guild_id": ctx.guild.id})
        number = 0
        embed = discord.Embed(title="Current AFK's", description="", color=self.constants.merx_embed_color_setup())

        async for afk in all_afks:
            number += 1
            embed.add_field(name=f"AFK Number: {number}", value=f"User: <@{afk.get('user_id')}>\nMessage: {afk.get('message')}", inline=False)
        
        if number == 0:
            embed = discord.Embed(title="Not Found", description="No AFK logs could be found for this server!", color=self.constants.merx_embed_color_setup())
        else:
            embed.set_footer(text=f"Moderator ID: {ctx.author.id} • Total AFK's: {number}")
        
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        afk_data = self.merx.afk_users

        afk_key = {'user_id': message.author.id, 'guild_id': message.guild.id}
        if afk_key in afk_data:
            
            await afks.delete_one({"user_id": message.author.id, 'guild_id': message.guild.id})
            await message.author.edit(nick=None)
            await message.reply(f"Your AFK has been ended!")
            self.merx.afk_users.remove(afk_key)
            return

        if message.mentions:
            for user in message.mentions:
                afk_key = {'user_id': user.id, 'guild_id': message.guild.id}
                if afk_key in afk_data:
                    result = await afks.find_one({'user_id': user.id, 'guild_id': message.guild.id})
                    await message.channel.send(embed=AfkEmbed(user, result.get('message')))

async def setup(merx):
    await merx.add_cog(AfkCommandCog(merx))