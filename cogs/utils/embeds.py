import discord
import platform
from discord import Interaction
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
from cogs.utils.constants import MerxConstants


# Success messages can use this embed by calling the class a passing correct prameters.

class SuccessEmbed(discord.Embed):
    def __init__(self, title: str, description: str, **kwargs):
        super().__init__(
            title=title, 
            description=description, 
            color=discord.Color.green(), 
            **kwargs
        )



# This is the error embed, call the errors.py file as well as this file and class to pass an error

class ErrorEmbed(discord.Embed):
    def __init__(self, error: Exception, error_id: str):
        super().__init__(
            title="Error Occurred",
            description=f"**Error ID:** `{error_id}`\n\n**Error Message:** ||{str(error)}||\n\n",
            color=discord.Color.red()
        )
        self.add_field(
            name="",
            value="If you need assistance, please contact support [here](https://discord.gg/nAX4yhVEgy)."
        )
        
        
        
# This is the permission denied embed, this will be used for things like admin commands or places where certain roles
# can only run the command, if they dont meet those requirements this will be sent instead.

class PermissionDeniedEmbed(discord.Embed):
    def __init__(self):
        super().__init__(
            title="Permission Denied",
            description="**Error Message** You do not have the required permissions to use this command.",
            color=discord.Color.red()
        )
        self.add_field(
            name="", 
            value="Please contact an admin if you believe this is an error."
        )
        


# This is the blacklist function for the blacklist system.

class BlacklistEmbed(discord.Embed):
    def __init__(self):
        super().__init__(
            title="Blacklist Notice",
            description="Your server or account is blacklisted and cannot use Merx.",
            color=discord.Color.red()
        )
        self.add_field(name="Reason", value="Please contact support [here](https://discord.gg/nAX4yhVEgy for more details.")
        
        
        
# This is an informative embed

class InfoEmbed(discord.Embed):
    def __init__(self, title: str, description: str, color: discord.Color, **kwargs):
        super().__init__(
            title=title, 
            description=description, 
            color=color, 
            **kwargs
        )



# This is for the start of the setup command also known as the disclaimer

class DisclaimerView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Continue", 
            style=discord.ButtonStyle.gray, 
            custom_id="continue")
        )
        
        
        self.add_item(discord.ui.Button(
            label="Exit", 
            style=discord.ButtonStyle.red, 
            custom_id="exit")
        )



# This is the setup options view and it includes buttons

class SetupOptionsView(discord.ui.View):
    def __init__(self, show_bot_config: bool, show_banner_config: bool):
        super().__init__()
        if show_bot_config:
            self.add_item(discord.ui.Button(
                label="Bot Config", 
                style=discord.ButtonStyle.gray, 
                custom_id="bot_config")
            )
           
            
        if show_banner_config:
            self.add_item(discord.ui.Button(
                label="Banner Config", 
                style=discord.ButtonStyle.gray, 
                custom_id="banner_config")
            )
            
            
        self.add_item(discord.ui.Button(label="Exit Setup", style=discord.ButtonStyle.red, custom_id="exit"))
        


# This is the embed for cancelling setup

class ExitSetupEmbed(discord.Embed):
    def __init__(self):
        super().__init__(
            title="Setup Canceled",
            description="The setup process has been canceled.",
            color=discord.Color.red()
        )
        
        

# This is for the new about command, edit the info for the command here instead of in the commands file.
# This allows replication late of info in the about command.

class AboutEmbed:
    @staticmethod
    def create_info_embed(uptime, guilds, users, latency, version, bot_name, bot_icon, thumbnail_url):
        embed = discord.Embed(
            description=(
                "Merx is an exceptional moderation and management tool designed specifically for community servers."
            ),
            color=discord.Color.from_str('#2a2c30')
        )


        embed.add_field(
            name="Merx Information",
            value=(
                f"> **Servers:** {guilds:,}\n"
                f"> **Users:** {users:,}\n"
                f"> **Uptime:** <t:{int((uptime.timestamp()))}:R>\n"
                f"> **Latency:** {round(latency * 1000)}ms"
            ),
            inline=False
        )


        embed.add_field(
            name="System Information",
            value=(
                f"> **Discord API Wrapper:** discord.py {discord.__version__}\n"
                f"> **Database System:** MongoDB {version}\n"
                f"> **Host OS:** {platform.system()}\n"
                f"> **Host:** Cali Web Design"
            ),
            inline=False
        )


        embed.set_author(name=bot_name, icon_url=bot_icon)
        embed.set_thumbnail(url=thumbnail_url)
        return embed
    
    

# This passes the about pages buttons with the embed so that these do not need to be recalled.

class AboutWithButtons:
    @staticmethod
    def create_view():
        view = View()

        async def commands_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            help_command = interaction.client.get_command('help')
            
            
            if help_command:
                await help_command(interaction)
            else:
                await interaction.response.send_message("Help command not found.", ephemeral=True)


        commands_button = Button(label="Commands", row=0, style=discord.ButtonStyle.primary, custom_id='commands_button')
        commands_button.callback = commands_callback
        view.add_item(commands_button)
        

        support_server_button = Button(
            label="Support Server", 
            style=discord.ButtonStyle.link, 
            url="https://discord.gg/nAX4yhVEgy"
        )
        
        
        invite_button = Button(
            label="Invite Merx", 
            style=discord.ButtonStyle.link, 
            url="https://discord.com/oauth2/authorize?client_id=1285105979947749406&permissions=8&integration_type=0&scope=bot"
        )


        view.add_item(support_server_button)
        view.add_item(invite_button)


        return view



# This is a debug command emebed that accepts parameters.    
    
class DebugEmbed(discord.Embed):
    def __init__(self, bot, ctx):
        
        
        # Creates a debug embed with various details for debugging purposes.
        
        super().__init__(
            title="Debug Information",
            description="Here is the current debug information for the Merx:",
            color=discord.Color.from_str('#dfa4ff')
        )


        # Define a dictionary with debug information fields
        
        fields = {
            "Latency": f"{round(bot.latency * 1000)} ms",
            "Server Name": ctx.guild.name,
            "Server ID": ctx.guild.id,
            "Channel": ctx.channel.name,
            "Channel ID": ctx.channel.id,
            "User": ctx.author.mention,
            "User ID": ctx.author.id
        }


        # Add all fields to the embed
        
        for name, value in fields.items():
            self.add_field(name=name, value=value, inline=True if "ID" in name else True)


        # Set footer with requesting user details
        
        self.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        
        
        
# This is the embed for the bots help center. This embed is the inital embed that shows that
# tells the user how to use the help center.

class HelpCenterEmbed(discord.Embed):
    def __init__(self, description: str, color: discord.Color = discord.Color.from_str('#dfa4ff')):
        super().__init__(
            title="Merx Help Center",
            description=description,
            color=color
        )
        
        
        
# This is the Nickname success embed. This will tell who was nicknamed, who nicknamed them,
# and what their previous and new name is. We do this in this file to allow it to be
# dynamic and edited once.

class NicknameSuccessEmbed(discord.Embed):
    def __init__(self, user, previous_name, new_name):
        super().__init__(
            title="Nickname Changed Successfully",
            description=(
                f"> **User**: {user.mention}\n"
                f"> **Previous Name**: ``{previous_name}``\n"
                f"> **New Name**: ``{new_name}``"
            ),
            color=discord.Color.green()
        )