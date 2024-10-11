import discord
import os
import requests
import asyncio
import sentry_sdk
from datetime import datetime
from discord.ext import commands
from utils.constants import MerxConstants, afks
from cogwatch import watch

# We use constants.py to specify things like the mongo db connnection, prefix
# and default embed color.

constants = MerxConstants()


class Merx(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = None
        self.start_time = datetime.now()
        self.beta_guilds = [
            1285107028892717118, # Merx Systems Discord
            1058691867484639232, # Feme's bot testing
            1283960722279239750, # 2nd testing guild for feme12
        ]
        
        
        
    @watch(path="cogs", preload=False)
    async def on_ready(self):
        merx.afk_users = []

        all_afks = afks.find({})
        async for afk in all_afks:
            afk_doc = {
                'user_id': afk.get('user_id'),
                'guild_id': afk.get('guild_id')
            }
            merx.afk_users.append(afk_doc)

        if constants.merx_environment_type() == "Development":
            for guild in merx.guilds:
                
                
                id = guild.id
                owner = guild.get_member(guild.owner_id)
                is_dev_guild = id in self.beta_guilds
                channel = merx.get_guild(self.beta_guilds[0]).get_channel(1289772928082378852)


                # Check if owner is None
                
                if owner is None:
                    owner_info = "Owner not found"
                else:
                    owner_info = f"{owner}({owner.id})"


                embed = discord.Embed(
                    title="Beta bot added to a guild",
                    description=f"**NAME:** `{guild.name}`\n**ID:** `{id}`\n**OWNER:** `{owner_info}`\n**IS_DEV_GUILD:** `{is_dev_guild}`"
                )


                if not is_dev_guild:
                    await guild.leave()
                    await channel.send(embed=embed)
                
        else:
            
            guild_count = len(merx.guilds)
            user_count = sum(guild.member_count for guild in merx.guilds)


            await merx.change_presence(activity=discord.Activity(
                name=f"{guild_count} Guilds • {user_count:,} Users • /help",
                type=discord.ActivityType.watching
            ))
            

        print(f"{merx.user.name} is ready!")#with {guild_count} guilds and {user_count:,} users.
            
            
        
    # Use bypassed users from the constants class instead of hardcoding them
    # The constants.py file will get the IDs from MongoDb allowing bot owners
    # to remove and add users.
        
    async def is_owner(self, user: discord.User):
        await constants.fetch_bypassed_users()
        return user.id in constants.bypassed_users



    # Sets up the cogs for Merx. This will cycle thru the cogs folder and
    # load each file with the .py file extenstion.
    
    async def setup_hook(self) -> None:
        for root, _, files in os.walk("./cogs"):
            for file in files:
                if file.endswith(".py"):
                    cog_path = os.path.relpath(os.path.join(root, file), "./cogs")
                    cog_module = cog_path.replace(os.sep, ".")[:-3]

                    await merx.load_extension(f"cogs.{cog_module}")

        print('All cogs loaded successfully!')
        
        
        
    async def refresh_blacklist_periodically(self):
        while True:
            await self.constants.refresh_blacklists()
            await asyncio.sleep(3600)


# Sets the bot's intents. This uses the members intent, default intents, and message_content
# intent. We will call intents later inorder to start Merx Bot.

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# Set bot prefix

prefix =  constants.prefix_setup


# Intializes Merx Bot and loads the prefix, intents, and other important things for discord.

merx = Merx(command_prefix=prefix,
            intents=intents,
            chunk_guilds_at_startup=False,
            help_command=None,
            allowed_mentions=discord.AllowedMentions(replied_user=True, everyone=True, roles=True))



# Before invoking any command, check blacklist.

@merx.before_invoke
async def before_invoke(ctx):
    
    
    # Skip check if the user is in the bypass list
    
    if ctx.author.id in constants.bypassed_users:
        return
    
    
    # Run the blacklist check
    
    await global_blacklist_check(ctx)



@merx.add_listener
async def on_message(message:discord.Message):
    if not f"{prefix}jsk" in message.content:
        return
    
    
    if await merx.is_owner(message.author):
        print(f"Jsk Ran by {message.author.name}({message.author.id}) message: '{message.content}'")

    
    
async def global_blacklist_check(ctx):
    

    # Fetch blacklist if not already fetched or periodically

    await constants.fetch_blacklisted_users()
    await constants.fetch_blacklisted_guilds()


    # Check if the user is blacklisted
    
    if ctx.author.id in constants.blacklists and ctx.command.name != "unblacklist":
        
        em = discord.Embed(
            title="Blacklisted",
            description="This user is blacklisted from Merx - Please appeal within our [Support Server](https://discord.gg/merxbot) or email `support@merxbot.xyz`!",
            color=constants.merx_embed_color_setup(),
        )
        
        await ctx.send(embed=em)
        
        raise commands.CheckFailure("You are blacklisted from using this bot.")


    # Check if the guild is blacklisted
    
    if ctx.guild and ctx.guild.id in constants.server_blacklists and ctx.command.name != "guild_unblacklist":
        
        em = discord.Embed(
            title="Blacklisted Guild",
            description="This server is blacklisted from Merx - Please appeal within our [Support Server](https://discord.gg/merxbot) or email `support@merxbot.xyz`!",
            color=constants.merx_embed_color_setup(),
        )
        
        await ctx.send(embed=em)
        
        raise commands.CheckFailure("This guild is blacklisted from using the bot.")


    # Prevent the command from being run in DMs
    
    if ctx.guild is None:
        raise commands.NoPrivateMessage("This command cannot be used in private messages.")

    return True



def run():
    
    # Sets up sentry for advanced error reporting. 
    # We use Cali Web Design's sentry account.
    
    sentry_sdk.init(
        dsn=constants.sentry_dsn_setup(),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    merx.run(constants.merx_token_setup())



if __name__ == "__main__":
    run()