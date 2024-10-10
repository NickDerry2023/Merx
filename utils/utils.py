import discord
from discord.ext import commands
from utils.constants import guild_counters

async def get_next_case_id(guild_id):
    
    guild_case_number = await guild_counters.find_one_and_update(
        {"_id": str(guild_id)},  # Search by guild ID
        {"$inc": {"seq": 1}},  # Increment the case ID by 1
        upsert=True,  # Create the document if it doesn't exist
        return_document=True  # Return the updated document
    )
    
    # Return the updated sequence number for this guild
    return guild_case_number["seq"]