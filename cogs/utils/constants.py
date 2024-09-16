import discord
from discord.ext import commands


class Constants(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bypassed_users = [895279150275903500, 1136153341580300288]  # User IDs
        self.blacklists = []
        self.server_blacklists = []

    async def is_owner(self, user: discord.User):
        return user.id in self.bypassed_users


async def setup(bot):
    await bot.add_cog(Constants(bot))
