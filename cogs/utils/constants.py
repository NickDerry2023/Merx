import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


class MerxConstants:
    def __init__(self):
        
        # Load environment variables when the class is initialized
        
        load_dotenv()
        
        # MongoDB setup variables
        
        self.mongo_client = None
        self.mongo_db = None
        
        # Bot-related constants
        
        self.bypassed_users = [895279150275903500, 1136153341580300288]  # User IDs
        self.blacklists = []
        self.server_blacklists = []
        
        
        
    # Checks the owner of the bot
    
    def is_owner(self, user_id: int):
        return user_id in self.bypassed_users



    # Setup MongoDB connection from environment variables
    
    async def mongo_setup(self):
        if self.mongo_client is None:
            self.mongo_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
            self.mongo_db = self.mongo_client[os.getenv('MONGODB_DATABASE')]



    # A method to ensure MongoDB setup has been called
    
    async def call_mongo_run(self):
        await self.mongo_setup()



    # Fetch the customizable prefix for the bot
    
    def prefix_setup(self):
        return os.getenv('PREFIX', 'm-')  # Return default prefix '-' if not set



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
        DEFAULT_EMBED_COLOR = os.getenv('MERX_EMBED_COLOR')
        return DEFAULT_EMBED_COLOR if DEFAULT_EMBED_COLOR else "0x00FF00" 
