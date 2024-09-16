import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


# Initialization of dotenv and the mongo variables and any other variables and set them to None

load_dotenv()
mongo_client = None
mongo_db = None


# This will setup mongo and get the mongo atributes from the ENV file so that the bot can use them
# this includes things like the Mongo DB database and Mongo DB URL

async def mongo_setup():
    global mongo_client, mongo_db
    if mongo_client is None:  # Initialize the client if not already done
        mongo_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
        mongo_db = mongo_client[os.getenv('MONGODB_DATABASE')]
        
        
async def call_mongo_run():
    await mongo_setup()


# This gets the custamizable refix based on the guild and what is set either during the servers
# setup or by the Merx Web Dashboard. This is now database set with - as a fallback incase the
# database isnt reachable or the bot isnt setup yet.

def prefix_setup():
    return os.getenv('PREFIX')


# This sets the token for the bot and the Sentry DSN so that Advanced error reporting can happen

def merx_token_setup():
    return os.getenv('TOKEN')

def sentry_dsn_setup():
    return os.getenv('SENTRY_DSN')

def merx_embed_color_setup():
    DEFAULT_EMBED_COLOR = os.getenv('MERX_EMBED_COLOR')
    return DEFAULT_EMBED_COLOR