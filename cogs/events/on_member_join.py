import discord
from discord.ext import commands
from discord.ui import View, Button
from utils.constants import MerxConstants

CHANNEL_NAME_FOR_WELCOME = ["chat", "general"]
constants = MerxConstants()

class OnMemberJoin(commands.Cog):
    def __init__(self, merx:commands.Bot):
        self.merx = merx
            

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
                global view
                view = None
                guild = self.merx.get_guild(1285107028892717118)

                try:# Code for staff tags
                    guild_member = await guild.fetch_member(member.id)

                    staff_roles = [
                        1285107029093912637, # Merx Team
                        1285107029093912636, # Development Team
                        1286165370926792806, # Management Team
                        1285107029060489232, # Management 2
                        1285107029005959206, # Support Team
                    ]

                    for role_id in staff_roles:
                        if discord.utils.get(guild_member.roles, id=role_id):
                            view = View().add_item(Button(label="Merx Staff", emoji="<:Merx:1290733278885576724>", disabled=True, style=discord.ButtonStyle.grey))
                            break

                except discord.NotFound:
                    print("Member not found.")
                except discord.Forbidden:
                    print("Bot does not have permission to fetch this member.")
                except Exception as e:
                    print(f"Error running the role check: {e}")

                            


            member_count = member.guild.member_count
            await welcome_channel.send(f"{member.mention} Welcome to **{member.guild.name}**! Feel free to explore. We now have **{member_count}** members. 🎉", view=view)         
                

async def setup(merx):
  await merx.add_cog(OnMemberJoin(merx))
