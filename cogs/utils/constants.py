import os
import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


class MerxConstants:
    def __init__(self):
        load_dotenv()
        self.mongo_client = None
        self.mongo_db = None
        self.bypassed_users = []
        self.blacklists = []
        self.server_blacklists = []
        

    # Setup MongoDB connection from environment variables
    
    async def mongo_setup(self):
        if self.mongo_client is None:
            try:
                mongodb_url = os.getenv('MONGODB_URL')
                mongodb_db = os.getenv('MONGODB_DB')

                if not mongodb_url or not mongodb_db:
                    print("MongoDB URL or Database name not found in environment variables.")
                    return None


                self.mongo_client = AsyncIOMotorClient(mongodb_url)
                self.mongo_db = self.mongo_client[mongodb_db]


                # Test the connection by running a simple command
                
                await self.mongo_db.command("ping")
                print("Successfully connected to MongoDB.")
                
                
            except Exception as e:
                print(f"Failed to connect to MongoDB: {str(e)}")
                return None

        return self.mongo_db
    
    
    # Checks the users to see if they are blacklist bypasssed and bot owner. This function
    # will get the User IDs from MongoDB and can be called to see if users are allowed to
    # run commands.
    
    async def fetch_bypassed_users(self):
        if self.mongo_db is None:
            await self.mongo_setup()

        try:
            collection = self.mongo_db["blacklist_bypass"]
            cursor = collection.find({}, {"discord_id": 1})
            bypassed_users = []
            async for document in cursor:
                bypassed_users.append(document["discord_id"])

            self.bypassed_users = bypassed_users

        except Exception as e:
            print(f"Error fetching bypassed users: {str(e)}")
    
    
    # Checks the owner of the bot
    # Owners will also be given Jsk Permissions which is dangerous so please be careful who you add into
    # the bot as an owner.
    
    async def is_owner(self, user_id: int):
        if not self.bypassed_users:
            await self.fetch_bypassed_users()
        return user_id in self.bypassed_users


    # Fetch the customizable prefix for the bot
    
    def prefix_setup(self):
        return os.getenv('PREFIX')  # Return default prefix '-' if not set


    # Fetch the bot token
    
    def merx_token_setup(self):
        token = os.getenv('TOKEN')
        if not isinstance(token, str):
            raise TypeError(f'expected token to be a str, received {type(token).__name__} instead')
        return token


    # Fetch the Sentry DSN for error reporting
    
    def sentry_dsn_setup(self):
        return os.getenv('SENTRY_DSN')


    # Fetch the default embed color for the bot
    
    def merx_embed_color_setup(self):
        DEFAULT_EMBED_COLOR = discord.Color.from_str('#dfa4ff')
        return DEFAULT_EMBED_COLOR


    # Gets the bots type either production or development

    def merx_environment_type(self):
        return os.getenv('ENVIRONMENT')
    
    
    
    async def fetch_blacklisted_users(self):
        
        
        if self.mongo_db is None:
            await self.mongo_setup()
            
            
        try:
            collection = self.mongo_db["blacklists"]
            cursor = collection.find({}, {"discord_id": 1})
            
            
            blacklists = []
            
            
            async for document in cursor:
                blacklists.append(document["discord_id"])
            self.blacklists = blacklists
            
            
        except Exception as e:
            print(f"Error fetching blacklisted users: {str(e)}")



    async def fetch_blacklisted_guilds(self):
        
        
        if self.mongo_db is None:
            await self.mongo_setup()
            
            
        try:
            collection = self.mongo_db["blacklists"]
            cursor = collection.find({}, {"guild_id": 1})
            server_blacklists = []
            
            
            async for document in cursor:
                server_blacklists.append(document["guild_id"])
            self.server_blacklists = server_blacklists
            
            
        except Exception as e:
            print(f"Error fetching blacklisted guilds: {str(e)}")



    # Call this periodically to refresh blacklist data
    
    async def refresh_blacklists(self):
        await self.fetch_blacklisted_users()
        await self.fetch_blacklisted_guilds()
        
        

    async def global_blacklist_check(ctx):
    

        # Fetch blacklist if not already fetched or periodically
        
        if not constants.blacklists:
            await constants.fetch_blacklisted_users()

        if not constants.server_blacklists:
            await constants.fetch_blacklisted_guilds()


        # Check if the user is blacklisted
        
        if ctx.author.id in constants.blacklists and ctx.command.name != "unblacklist":
            
            em = discord.Embed(
                title="Blacklisted",
                description="You are blacklisted from Merx - please appeal within our [support server](https://discord.gg/nAX4yhVEgy)!",
                color=discord.Color(int('fecb02', 16)),
            )
            
            await ctx.send(embed=em)
            
            raise commands.CheckFailure("You are blacklisted from using this bot.")


        # Check if the guild is blacklisted
        
        if ctx.guild and ctx.guild.id in constants.server_blacklists and ctx.command.name != "guild_unblacklist":
            
            em = discord.Embed(
                title="Blacklisted Guild",
                description="This server is blacklisted from Merx - please appeal within our [support server](https://discord.gg/nAX4yhVEgy)!",
                color=discord.Color(int('fecb02', 16)),
            )
            
            await ctx.send(embed=em)
            
            raise commands.CheckFailure("This guild is blacklisted from using the bot.")


        # Prevent the command from being run in DMs
        
        if ctx.guild is None:
            raise commands.NoPrivateMessage("This command cannot be used in private messages.")

        return True