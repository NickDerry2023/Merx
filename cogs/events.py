import discord
import datetime
import time
import json
import os
import uuid
import shortuuid
from discord import Embed
from discord.ext import tasks, commands
from discord.ext.commands.context import Context
from cogs.utils.constants import MerxConstants



CHANNEL_NAME_FOR_WELCOME = ["chat", "general"]
constants = MerxConstants()


class MerxEvents(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.change_status.start()
        self.beta_guilds = [
            1285107028892717118, # Merx Systems Discord
        ]
        
        
    
    # This starts the activity and gets the users and guilds and sets it initally.
    
    @commands.Cog.listener()
    async def on_ready(self):
        guild_count = len(self.merx.guilds)
        user_count = sum(guild.member_count for guild in self.merx.guilds)

        await self.merx.change_presence(activity=discord.Activity(
            name=f"{guild_count} Guilds • {user_count:,} Users • /help",
            type=discord.ActivityType.watching
        ))

        print(f"{self.merx.user.name} is ready with {guild_count} guilds and {user_count:,} users.")
        
        


    if constants.merx_environment_type() == "Development":
        @commands.Cog.listener()
        async def on_ready(self):
            for guild in self.merx.guilds:
                id = guild.id
                owner = guild.get_member(guild.owner_id)
                is_dev_guild = id in self.beta_guilds
                channel = self.merx.get_guild(self.beta_guilds[0]).get_channel(1289772928082378852)

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
                    


        @commands.Cog.listener()
        async def on_guild_join(self, guild: discord.Guild):
            id = guild.id
            owner = guild.get_member(guild.owner_id)
            is_dev_guild = id in self.beta_guilds
            channel = self.merx.get_guild(self.beta_guilds[0]).get_channel(1289772928082378852)

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



    # This updated the guilds and users periodically every 30 seconds.

    @tasks.loop(seconds=30)
    async def change_status(self):
        guild_count = len(self.merx.guilds)
        user_count = sum(guild.member_count for guild in self.merx.guilds)


        await self.merx.change_presence(activity=discord.Activity(
            name=f"{guild_count} Guilds • {user_count:,} Users • /help",
            type=discord.ActivityType.watching
        ))
            


    if constants.merx_environment_type() == "Production":
        @commands.Cog.listener()
        async def on_member_join(self, member: discord.Member):
            welcome_channel = discord.utils.get(member.guild.text_channels, name=CHANNEL_NAME_FOR_WELCOME)
            welcome_channel = None
            for channel_name in CHANNEL_NAME_FOR_WELCOME:
                welcome_channel = discord.utils.get(member.guild.text_channels, name=channel_name)
                if welcome_channel:
                    break
            
            if welcome_channel:
                member_count = member.guild.member_count
                await welcome_channel.send(f"{member.mention} Welcome to **{member.guild.name}**! Feel free to explore. We now have **{member_count}** members. 🎉")         
                

async def setup(merx):
  await merx.add_cog(MerxEvents(merx))