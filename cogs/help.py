import discord
from discord.ext import commands
from discord.ui import Button, View
import DiscordUtils
from cogs.utils.errors import send_error_embed
from cogs.utils.constants import MerxConstants
import asyncio


constants = MerxConstants()


DEFAULT_EMBED_COLOR = discord.Color.from_str('#dfa4ff')
EXCLUDED_COMMANDS = ['jishaku', 'debug', 'add_owner', 'remove_owner', 'sync']


# This is the help command area, this will list possible commands that you can use within LCU. The plan
# for this command is to allow users to search, and move about different pages commands will be on. Each page
# will be titled with a main page showing common commands.

class HelpCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx


    @commands.hybrid_command(description="Provides tons of information on the bots commands and how to use them.", with_app_command=True, extras={"category": "Help"})
    async def help(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)
        
        
        # This sets the count of commands per page and sets the default page for pagination
        
        commands_per_page = 15
        self.commands = [cmd for cmd in self.merx.commands if isinstance(cmd, commands.HybridCommand) or isinstance(cmd, commands.Command)]
        self.total_pages = (len(self.commands) // commands_per_page) + 1
        self.current_page = 1
        
        
        # Makes the commands clickable and slash commands with IDS (may or may have not taken from prod once and refactored it)
        
        self.command_ids = {}
        for command in await self.merx.tree.fetch_commands():
            for child in command.options:
                self.command_ids[f"{command.name} {child.name}"] = {
                    'id': command.id,
                    'description': str(child.description)
                }
            self.command_ids[command.name] = {
                'id': command.id,
                'description': command.description
            }


        # Define the embed generation function inside the class to access class-level variables
        
        def get_embed(page: int, search_query: str = '') -> discord.Embed:
            embed = discord.Embed(
                title=f"Merx Help Center | {self.get_category_name(page)}",
                description="",
                color=discord.Color.from_str('#dfa4ff')
            )
            commands_list = self.get_commands_list(page, commands_per_page, search_query)
            embed.add_field(
                name="",
                value=commands_list or "No commands available.",
                inline=False
            )
            return embed
        

        # Define the view class with its methods
        
        class HelpButtons(View):
            def __init__(self, page: int, total_pages: int, ctx: commands.Context, commands: list, search_query: str = ''):
                super().__init__()
                self.page = page
                self.total_pages = total_pages
                self.ctx = ctx
                self.commands = commands
                self.search_query = search_query
                
                
            # This is the button for previous to go back a page.
            
            @discord.ui.button(label="Previous", style=discord.ButtonStyle.grey, disabled=True)
            async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
                if self.page > 1:
                    self.page -= 1
                    await self.update_message()
                    
                    
            # This is the button for next to go forward a page.
            
            @discord.ui.button(label="Next", style=discord.ButtonStyle.grey, disabled=True)
            async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
                if self.page < self.total_pages:
                    self.page += 1
                    await self.update_message()
                    
                    
            # This is the search button to search commands as well as the logic to perform the search.
            
            @discord.ui.button(label="Search", style=discord.ButtonStyle.primary)
            async def search(self, button: discord.ui.Button, interaction: discord.Interaction):
                await interaction.response.send_message("Please enter a search query:", ephemeral=True)
                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.TextChannel)
                try:
                    search_msg = await self.ctx.merx.wait_for('message', timeout=60.0, check=check)
                    self.search_query = search_msg.content
                    await search_msg.delete()
                    await self.update_message()
                except asyncio.TimeoutError as e:
                    error_id = str(uuid.uuid4())
                    await send_error_embed(interaction, e, error_id)


            # This will update the Discord message.
            
            async def update_message(self):
                embed = get_embed(self.page, self.search_query)
                if self.page == 1:
                    self.children[0].disabled = True
                else:
                    self.children[0].disabled = False
                if self.page == self.total_pages:
                    self.children[1].disabled = True
                else:
                    self.children[1].disabled = False
                await self.message.edit(embed=embed, view=self)


        # Outputs the buttons to the Discord UI
        
        view = HelpButtons(self.current_page, self.total_pages, ctx, self.commands)
        embed = get_embed(self.current_page)
        message = await ctx.send(embed=embed, view=view)
        view.message = message
        
        
    # Function to get the list of available commands and also exclude special commands the owner doesn't want
    
    def get_commands_list(self, page: int, commands_per_page: int, search_query: str = '') -> str:
        commands_list = ""


        if search_query:
            commands = [cmd for cmd in self.commands if search_query.lower() in cmd.name.lower()]
        else:
            commands = [cmd for cmd in self.commands if cmd.name not in EXCLUDED_COMMANDS]


        # Actual command logic
        
        start = (page - 1) * commands_per_page
        end = start + commands_per_page
        for command in commands[start:end]:
            command_name = command.qualified_name
            command_description = command.description or 'No description provided.'
            command_id = self.command_ids.get(command_name, {}).get('id', 'Unknown ID')
            commands_list += f"</{command_name}:{command_id}> - {command_description}\n\n"
        return commands_list.strip()


    # Gets the command category for the help center header instead of doing page numbers just as how production does it.

    def get_category_name(self, page: int) -> str:
        categories = {}
        for command in self.merx.commands:
            if isinstance(command, commands.HybridCommand) or isinstance(command, commands.Command):
                category = command.extras.get('category', 'General')
                if category not in categories:
                    categories[category] = []
                categories[category].append(command)


        # List the catagory, if one isnt known then its thrown with an unknown error.

        category_list = list(categories.keys())
        if 1 <= page <= len(category_list):
            return category_list[page - 1]
        return "Unknown"
        

async def setup(merx):
    await merx.add_cog(HelpCommandsCog(merx))
