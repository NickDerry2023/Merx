import discord
import datetime
import time
import json
import os
from discord.ext import tasks, commands
from discord.ext.commands.context import Context


class MerxEvents(commands.Cog):
    def __init__(self, merx):
        self.merx = merx

    @commands.Cog.listener()
    async def on_ready(self, ctx: commands.Context = None):
        await self.merx.change_presence(activity=discord.Activity(name="m-help | merxbot.xyz", type=discord.ActivityType.watching))
        print(self.merx.user.name + " is ready.")
            

async def setup(merx):
  await merx.add_cog(MerxEvents(merx))