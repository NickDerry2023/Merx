import discord
from discord import Embed
from discord.ext import commands

class OnGuildJoin(commands.Cog):
    def __init__(self, merx):
        self.merx = merx

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        id = guild.id
        owner = guild.get_member(guild.owner_id)
        is_dev_guild = id in self.merx.beta_guilds
        channel = self.merx.get_guild(self.merx.beta_guilds[0]).get_channel(1289772928082378852)

        # Check if owner is None
        if owner is None:
            owner_info = "Owner not found"
        else:
            owner_info = f"{owner}({owner.id})"

        embed = Embed(
            title="Beta bot added to a guild",
            description=f"**NAME:** `{guild.name}`\n**ID:** `{id}`\n**OWNER:** `{owner_info}`\n**IS_DEV_GUILD:** `{is_dev_guild}`"
        )

        if not is_dev_guild:
            await guild.leave()
        
        await channel.send(embed=embed)
 
async def setup(merx):
  await merx.add_cog(OnGuildJoin(merx))