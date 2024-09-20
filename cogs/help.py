import discord
import asyncio
import uuid
import shortuuid
from discord.ext import commands
from discord.ui import Select, View
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import HelpCenterEmbed


# Brand new help command that uses a drop down and hidden messages to display content in
# a cleaner way. This was taken as inspiration from Lukas (notlukasrx)

constants = MerxConstants()

EXCLUDED_COMMANDS = ['jishaku', 'debug', 'add_owner', 'remove_owner', 'sync']


# This is the help cog that shows how to use the bot a list of its commands.

class HelpCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.categories = self.get_command_categories()
        

    @commands.hybrid_command(description="Provides information on the bot's commands and how to use them.", with_app_command=True, extras={"category": "Help"})
    async def help(self, ctx: commands.Context):
        
        await ctx.defer(ephemeral=False)


        # Dropdown select for help topics, The user can select a help topic. This makes the help command
        # easier to read and use.
        
        class HelpDropdown(Select):
            
            def __init__(self, categories, merx):
                self.merx = merx
                options = [discord.SelectOption(label=cat, description=f"See commands in {cat}") for cat in categories]
                super().__init__(placeholder="Select a help topic", options=options)


            # This finds the list of available commands and sends them to the user.

            async def callback(self, interaction: discord.Interaction):
                selected_category = self.values[0]
                command_list = self.get_commands_in_category(selected_category)


                embed = discord.Embed(
                    title=f"Commands for {selected_category}",
                    description=command_list or "No commands available.",
                    color=constants.merx_embed_color_setup()
                )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)


            # Gets the commands in the catagory and prepares them to be listed.

            def get_commands_in_category(self, category: str) -> str:
                command_list = ""
                commands_in_category = [cmd for cmd in self.merx.commands 
                                        if cmd.extras.get('category', 'General') == category
                                        and cmd.qualified_name not in EXCLUDED_COMMANDS]
                
                # Fetch all application commands (slash commands)
                
                slash_commands = {command.name: command for command in self.merx.tree.get_commands()}

                for command in commands_in_category:
                    command_name = command.qualified_name
                    command_description = command.description or 'No description provided.'

                    # Check if the command is a slash command and get its ID if it exists
                    
                    slash_command = slash_commands.get(command_name)
                    
                    # This will use slash commands when possible but then default to printing the commands
                    # if it can not get the commands id from discord.
                    
                    if slash_command and hasattr(slash_command, 'id') and slash_command.id:
                        command_list += f"</{command_name}:{slash_command.id}> - {command_description}\n"
                    else:
                        command_list += f"**/{command_name}** - {command_description}\n"

                return command_list.strip()


        # View with dropdown, This prepares and displays the main embed. This gets the embed from
        # embeds.py file and fills in the information.
        
        dropdown = HelpDropdown(self.categories, self.merx)
        view = View()
        view.add_item(dropdown)


        embed = HelpCenterEmbed(
            description="Welcome to Merx, select a help topic from the dropdown to view the commands. Once you find the command you want simply run it.",
            color=constants.merx_embed_color_setup()
        )
        
        
        await ctx.send(embed=embed, view=view)


    # This gets a list of the bots commands catagory.

    def get_command_categories(self) -> list:
        categories = set()
        for command in self.merx.commands:
            if isinstance(command, commands.HybridCommand) or isinstance(command, commands.Command):
                category = command.extras.get('category', 'General')
                categories.add(category)
        return sorted(categories)
    
    

async def setup(merx):
    await merx.add_cog(HelpCommandsCog(merx))
