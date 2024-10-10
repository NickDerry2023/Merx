import discord
from discord.ext import tasks, commands

class Tasks(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.change_status.start()

    @tasks.loop(seconds=30)
    async def change_status(self):
        guild_count = len(self.merx.guilds)
        user_count = sum(guild.member_count for guild in self.merx.guilds)


        await self.merx.change_presence(activity=discord.Activity(
            name=f"{guild_count} Guilds • {user_count:,} Users • /help",
            type=discord.ActivityType.watching
        ))      
                

async def setup(merx):
  await merx.add_cog(Tasks(merx))