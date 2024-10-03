import discord
import platform
from datetime import datetime
from discord import Interaction
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
from cogs.utils.constants import MerxConstants


constants = MerxConstants()


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
            description=f"**Error ID:** `{error_id}`\n\n**Error Message:** {str(error)}\n\n",
            color=discord.Color.red()
        )
        self.add_field(
            name="",
            value="If you need assistance, please contact support [here](https://discord.gg/merxbot)."
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
        self.add_field(name="Reason", value="Please contact support [here](https://discord.gg/merxbot for more details.")
        
        
        
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
    def create_info_embed(uptime, guilds, users, latency, version, bot_name, bot_icon, shards, cluster, environment, command_run_time, thumbnail_url):
        embed = discord.Embed(
            description=(
                "Merx is an exceptional moderation and management tool designed specifically for community servers."
            ),
            color=discord.Color.from_str('#2a2c30')
        )


        embed.add_field(name="",value=(""),inline=False)


        embed.add_field(
            name="Merx Information",
            value=(
                f"> **Servers:** {guilds:,}\n"
                f"> **Users:** {users:,}\n"
                f"> **Uptime:** <t:{int((uptime.timestamp()))}:R>\n"
                f"> **Latency:** {round(latency * 1000)}ms"
            ),
            inline=True
        )


        embed.add_field(
            name="System Information",
            value=(
                f"> **Language:** Python\n"
                f"> **Database:** MongoDB {version}\n"
                f"> **Host OS:** {platform.system()}\n"
                f"> **Host:** Cali Web Design"
            ),
            inline=True
        )
        
        
        embed.add_field(name="",value=(""),inline=False)
        
        
        embed.set_footer(
            text=f"Cluster {cluster} | Shard {shards} | {environment} • {command_run_time}"
        )


        embed.set_author(name=bot_name, icon_url=bot_icon)
        embed.set_thumbnail(url=thumbnail_url)
        return embed
    
    

# This passes the about pages buttons with the embed so that these do not need to be recalled.

class AboutWithButtons:
    @staticmethod
    def create_view():
        view = View()


        support_server_button = Button(
            label="Support Server", 
            style=discord.ButtonStyle.primary, 
            url="https://discord.gg/merxbot"
        )
        
        
        invite_button = Button(
            label="Invite Merx", 
            style=discord.ButtonStyle.link, 
            url="https://discord.com/oauth2/authorize?client_id=1285105545078116453&permissions=8&integration_type=0&scope=bot"
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
        
        
        
# This is the server information emebed logic, this will accept things like server roles, channel counts,
# emojies, and much more. This embed will also format it like circle does. Simply call this emebed then pass
# the correct parameters. 

class ServerInformationEmbed:
    
    
    def __init__(self, guild, constants):
        self.guild = guild
        self.constants = constants



    def create_embed(self):
        
        
        # Define the predefined values
        
        owner = self.guild.owner
        member_count = self.guild.member_count
        created_at = self.guild.created_at.strftime("%B %d, %Y")
        role_count = len(self.guild.roles)
        emoji_count = len(self.guild.emojis)
        text_channels = len(self.guild.text_channels)
        voice_channels = len(self.guild.voice_channels)
        announcement_channels = len([c for c in self.guild.channels if isinstance(c, discord.TextChannel) and c.is_news()])
        forum_channels = len(self.guild.forums)
        verification_level = str(self.guild.verification_level).capitalize()
        explicit_content_filter = str(self.guild.explicit_content_filter).replace('_', ' ').capitalize()
        two_factor_auth = "Enabled" if self.guild.mfa_level == 1 else "Disabled"
        boosts = self.guild.premium_subscription_count
        boost_tier = self.guild.premium_tier
        icon_url = self.guild.icon.url if self.guild.icon else None


        # Create the embed
        
        embed = discord.Embed(
            title=f"Server Info - {self.guild.name}",
            color=self.constants.merx_embed_color_setup(),
            timestamp=datetime.utcnow()
        )
        

        # Add fields to the embed
        
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="**Generic Information**", 
            value=f"> **Server Owner:** {owner}\n"
                  f"> **Member Count:** {member_count}\n"
                  f"> **Creation Date:** {created_at}\n"
                  f"> **Verification Level:** {verification_level}\n"
                  f"> **2FA Status:** {two_factor_auth}\n"
                  f"> **Explicit Content Filter:** {explicit_content_filter}", 
            inline=False
        )
        
        
        embed.add_field(
            name="Channels",
            value=f"> Text: {text_channels}\n > Voice: {voice_channels}\n > Announcements: {announcement_channels}\n > Forum: {forum_channels}",
            inline=False
        )


        # Roles
        
        roles_list = ', '.join([role.mention for role in self.guild.roles[1:20]])
        if role_count > 20:
            roles_list += f"... and {role_count - 20} more roles."
        embed.add_field(name=f"Roles ({role_count})", value=roles_list, inline=False)


        # Emojis
        
        emoji_list = ', '.join([str(emoji) for emoji in self.guild.emojis[:20]])
        if emoji_count > 20:
            emoji_list += f"... and {emoji_count - 20} more emojis."
        embed.add_field(name=f"Emojis ({emoji_count})", value=emoji_list, inline=False)


        # Boost info
        
        embed.add_field(name="Boosts", value=f"> {boosts} (Tier {boost_tier})", inline=False)


        return embed
    
    

# This is the role success emebed for when a action is performed with roles.
    
class RoleSuccessEmbed(discord.Embed):
    def __init__(self, title: str, description: str):
        super().__init__(title=title, description=description, color=discord.Color.green())
        
        
        
# This is the channel success emebed for when channel and category functions are used.        
        
class ChannelSuccessEmbed(discord.Embed):
    def __init__(self, title: str, description: str):
        super().__init__(title=title, description=description, color=discord.Color.green())
        
        

class SearchResultEmbed(discord.Embed):
    def __init__(self, title: str, description: str, case_number: int, collection: str, details: str):
        super().__init__(title=title, description=description, color=constants.merx_embed_color_setup())
        self.add_field(name="Case Number", value=case_number, inline=False)
        self.add_field(name="Collection", value=collection, inline=False)
        self.add_field(name="Details", value=details, inline=False)
        
      
 
# This contains the emebed and its parameters for the ping command. This shows things like uptime,
# latency to discors and mongodb.        
        
class PingCommandEmbed(discord.Embed):
    def create_ping_embed(latency, database_latency, uptime, version):
        embed = discord.Embed(
            title="",
            color=discord.Color.green()
        )

        
        embed.add_field(
            name="**🏓 Pong!**", 
            value=f"> **Latency:** {round(latency * 1000)}ms\n"
                  f"> **Database Latency:** {database_latency}ms\n"
                  f"> **Uptime:** <t:{int((uptime.timestamp()))}:R>\n"
                  f"> **Build Version:** {version}\n",
            inline=False
        )


        return embed
    
    
    
# This is the embed for User Information command also known as whois. 

class UserInformationEmbed:
    def __init__(self, member, constants):
        self.member = member
        self.constants = constants



    def create_embed(self):


        user_mention = self.member.mention
        display_name = self.member.display_name
        user_id = self.member.id
        account_created = f"<t:{int(self.member.created_at.timestamp())}:F>"
        joined_server = f"<t:{int(self.member.joined_at.timestamp())}:F>" if self.member.joined_at else "N/A"
        roles = [role.mention for role in self.member.roles if role.name != "@everyone"]
        role_count = len(roles)
        
        
        badges = []
        flags = self.member.public_flags


        if flags.hypesquad_bravery:
            badges.append("> <:houseBravery:1287991028950761523> HypeSquad Bravery")
        if flags.hypesquad_brilliance:
            badges.append("> <:houseBrilliance:1287990589773840416> HypeSquad Brilliance")
        if flags.hypesquad_balance:
            badges.append("> <:houseBalance:1287990232591106069> HypeSquad Balance")
        if flags.verified_bot:
            badges.append("> <:verified:1287994141036384330> Verified Bot")
        if flags.early_supporter:
            badges.append("> <:EarlyVerifiedDeveloperBadge:1287990726751162368> Early Supporter")
        if flags.active_developer:
            badges.append("> <:DeveloperBadge:1287990849640075318> Active Developer")


        embed = discord.Embed(
            title=f"User Info - {display_name}",
            color=self.constants.merx_embed_color_setup(),
            timestamp=datetime.utcnow()
        )


        embed.add_field(
            name="**User Information**", 
            value=f"> **Mention:** {user_mention}\n"
                  f"> **Display Name:** {display_name}\n"
                  f"> **User ID:** {user_id}\n"
                  f"> **Account Created:** {account_created}\n"
                  f"> **Joined Server:** {joined_server}", 
            inline=False
        )


        if badges:
            embed.add_field(name="Badges", value='\n'.join(badges), inline=False)
        else:
            embed.add_field(name="Badges", value="No badges", inline=False)
            

        embed.add_field(name=f"Roles ({role_count})", value=', '.join(roles) if roles else "No Roles", inline=False)


        if self.member.bot:
            embed.set_footer(text="This user is a bot.")
            

        return embed



class CheckGuildEmbed(discord.Embed):
    def create_valid_guild_embed(self, guild: discord.Guild):
        embed = discord.Embed(
            title="Valid Guild",
            description="I have found that guild here is the information on it.",
            color=self.constants.merx_embed_color_setup()
        )
        owner = guild.owner
        member_count = guild.member_count
        created_at = guild.created_at.strftime("%B %d, %Y")
        boosts = guild.premium_subscription_count
        boost_tier = guild.premium_tier
        icon_url = guild.icon.url if guild.icon else None

        embed.add_field(
            name="Information",
            value=f"> **Name:** {guild.name}\n"
            f"> **Server Owner:** {owner}"
            f"> **Member Count:** {member_count}"
            f"> **Created At:** {created_at}"
            f"> **Boosts:** {boosts}"
            f"> **Boost Tier:** {boost_tier}"
        )
        embed.set_thumbnail(url=icon_url)

        return embed
    def create_invalid_guild_embed(id):
        embed = discord.Embed(
            title="Invalid Guild",
            description=f"The guild by the id of ({id})",
            color=discord.Color.red()
        )

        return embed
    
    
# This specifices the afk emebed error, telling use
    
class AfkEmbed(discord.Embed):
    
    
    def __init__(self, user: discord.User, reason: str):
        super().__init__(
            title=f"{user.name} is currently AFK",
            description=f"> Reason: {reason}",
            color=constants.merx_embed_color_setup()
        )
        
        
        self.set_footer(text="They will respond when they are back.")


class EmojiFindEmbed:
    def __init__(self, emoji):
        self.emoji = emoji
        self.constants = constants
    
    def create_embed(self):
        emoji_guild = self.emoji.guild
        emoji_name = self.emoji.name
        emoji_animated = self.emoji.animated
        emoji_created = self.emoji.created_at.timestamp()
        emoji_id = self.emoji.id
        emoji_url = self.emoji.url


        embed = discord.Embed(
            title="",
            description=f"**Name**\n> {emoji_name}\n\n**Id**\n> {emoji_id}\n\n**Animated**\n> {emoji_animated}\n\n**Created**\n> <t:{int(emoji_created)}:f>",
            color=self.constants.merx_embed_color_setup()
        )


        embed.set_author(name=f"{emoji_guild} emoji.", icon_url=emoji_guild.icon.url)
        embed.set_thumbnail(url=emoji_url)

        return embed
    
    

# This is the embed for the Auto Moderation feature that gets the list of banned words from
# Mongo Db then lists it in a nice way.

class AutoModListWordsEmbed(discord.Embed):
    def __init__(self, guild_name: str, banned_words: str, color: discord.Color):
        super().__init__(title=f"Banned Words for {guild_name}", color=color)
        self.add_field(name="Banned Words", value=banned_words, inline=False)
        self.set_footer(text=f"Total words: {len(banned_words.split(', '))}")
        
        
        
# This is the embed that shows the current prefix for the bot.
        
class PrefixEmbed(discord.Embed):
    def __init__(self, current_prefix: str):
        super().__init__(
            title="",
            description=f"The current prefix for this server is `{current_prefix}`.",
            color=constants.merx_embed_color_setup()
        )



# This is the success embed when the bots prefix is successfully changed by the user.

class PrefixSuccessEmbed(discord.Embed):
    def __init__(self, new_prefix: str):
        super().__init__(
            title="",
            description=f"<:whitecheck:1285350764595773451> Prefix successfully changed to `{new_prefix}`.",
            color=discord.Color.green()
        )
        
        
        
# This is the reminders success embed that shows when a reminder is successfully set.

class ReminderEmbed(discord.Embed):
    def __init__(self, reminder_time: str, **kwargs):
        super().__init__(**kwargs)

        # Set the embed title and color
        self.title = ""
        self.description = f"<:whitecheck:1285350764595773451> Got it! I have set a reminder. It will go off at **{reminder_time}**."
        self.color = discord.Color.green()