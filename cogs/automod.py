import discord
import asyncio
import time
from discord.ext import commands
from collections import defaultdict
from cogs.utils.embeds import DebugEmbed, PermissionDeniedEmbed, SuccessEmbed
from cogs.utils.constants import MerxConstants
from cogs.utils.errors import send_error_embed


constants = MerxConstants()


class AutoModCommandCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.banned_words = []  # This will be fetched from MongoDB
        self.message_log_channel_id = None  # This will also be fetched from MongoDB
        self.user_message_tracker = defaultdict(list)



    async def cog_load(self):
        

        mongo_db = await constants.mongo_setup()

        if mongo_db is None:

            
            print("Failed to connect to the database.")
            return


        # Fetch blacklisted words and log channel after ensuring MongoDB connection is established
        
        await self.fetch_banned_words(mongo_db)
        await self.fetch_logging_channel(mongo_db)



    async def fetch_banned_words(self, mongo_db):


        blacklistedwords_collection = mongo_db["blacklistedwords"]
        banned_words_docs = await blacklistedwords_collection.find().to_list(length=100)
        
        self.banned_words = [doc['word'] for doc in banned_words_docs if 'word' in doc]



    async def fetch_logging_channel(self, mongo_db):
 
 
        setup_collection = mongo_db["setup"]
        setup_data = await setup_collection.find_one({"logging_channel": {"$exists": True}})
        
        
        if setup_data:
            self.message_log_channel_id = setup_data.get("logging_channel")
        else:
            print("No logging channel found in the database.")



    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await self.check_for_banned_words(message)
        await self.detect_spam(message)
        await self.log_message(message)



    async def check_for_banned_words(self, message):
        
        
        content = message.content.lower()
        
        
        for word in self.banned_words:
            if word in content:
                await message.delete()
                try:
                    await message.author.send(f"Your message in **{message.guild.name}** contained inappropriate content and was removed.")
                except discord.Forbidden:
                    await message.channel.send(f"{message.author.mention}, your message contained inappropriate content and was removed.")



    async def detect_spam(self, message):
        
        
        current_time = time.time()
        self.user_message_tracker[message.author.id].append(current_time)


        self.user_message_tracker[message.author.id] = [t for t in self.user_message_tracker[message.author.id] if current_time - t < 10]


        if len(self.user_message_tracker[message.author.id]) > 5:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you're sending messages too quickly. Please slow down.")
            await self.log_moderation_action(message, "Spam detected")



    async def log_message(self, message):
        
        
        if not self.message_log_channel_id:
            return
        

        log_channel = self.merx.get_channel(self.message_log_channel_id)
        if log_channel:
            embed = discord.Embed(title="Message Logged", color=discord.Color.blue())
            embed.add_field(name="User", value=message.author.mention)
            embed.add_field(name="Channel", value=message.channel.mention)
            embed.add_field(name="Content", value=message.content, inline=False)
            embed.timestamp = message.created_at
            await log_channel.send(embed=embed)



    async def log_moderation_action(self, message, reason):
        
        
        if not self.message_log_channel_id:
            return


        log_channel = self.merx.get_channel(self.message_log_channel_id)
        if log_channel:
            embed = discord.Embed(title="Moderation Action", color=discord.Color.red())
            embed.add_field(name="User", value=message.author.mention)
            embed.add_field(name="Channel", value=message.channel.mention)
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Content", value=message.content, inline=False)
            embed.timestamp = message.created_at
            await log_channel.send(embed=embed)
            
     
    
    @commands.hybrid_command(name="addword", description="Add a word to the banned words list (Admin only)")
    @commands.has_permissions(administrator=True)  # Check if the user has admin permissions
    async def add_word(self, ctx: commands.Context, word: str):
    
        
        mongo_db = await constants.mongo_setup()
        
        
        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return

        
        await self.add_banned_word(mongo_db, word)
        await ctx.send(f"<:whitecheck:1285350764595773451> The word `{word}` has been added to the banned words list.")


    
    @commands.hybrid_command(name="removeword", description="Remove a word from the banned words list (Admin only)")
    @commands.has_permissions(administrator=True)
    async def remove_word(self, ctx: commands.Context, word: str):


        mongo_db = await constants.mongo_setup()


        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return

        
        await self.remove_banned_word(mongo_db, word)
        await ctx.send(f"<:whitecheck:1285350764595773451> The word `{word}` has been removed from the banned words list.")

    
    
    @commands.hybrid_command(name="listwords", description="Remove a word from the banned words list (Admin only)")
    async def list_banned_words(self, interaction: discord.Interaction):
        
        
        if not self.banned_words:
            await interaction.response.send_message("<:xmark:1285350796841582612> No banned words found.", ephemeral=True)
            return


        banned_words_str = ', '.join(self.banned_words)
        await interaction.response.send_message(f"<:xmark:1285350796841582612> Banned words: {banned_words_str}", ephemeral=True)
        
        
    
    async def fetch_banned_words(self, mongo_db):
        blacklistedwords_collection = mongo_db["blacklistedwords"]
        banned_words_docs = await blacklistedwords_collection.find().to_list(length=100)
        self.banned_words = [doc['word'] for doc in banned_words_docs if 'word' in doc]



    async def add_banned_word(self, mongo_db, word):
        blacklistedwords_collection = mongo_db["blacklistedwords"]
        await blacklistedwords_collection.insert_one({'word': word})
        await self.fetch_banned_words(mongo_db)



    async def remove_banned_word(self, mongo_db, word):
        blacklistedwords_collection = mongo_db["blacklistedwords"]
        await blacklistedwords_collection.delete_one({'word': word})
        await self.fetch_banned_words(mongo_db)



async def setup(merx):
    await merx.add_cog(AutoModCommandCog(merx))
