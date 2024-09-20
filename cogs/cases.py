import discord
from datetime import datetime
from discord.ext import commands
from cogs.utils.constants import MerxConstants
from cogs.utils.embeds import SearchResultEmbed, ErrorEmbed
from cogs.utils.errors import send_error_embed

constants = MerxConstants()

class CaseSearchCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.constants = MerxConstants()  # Access constants for MongoDB setup



    @commands.hybrid_command(name="case", description="Searches cases by an Case ID.", with_app_command=True)
    async def case(self, ctx, case_id: int):


        mongo_db = await self.constants.mongo_setup()


        if mongo_db is None:
            await ctx.send("<:xmark:1285350796841582612> Failed to connect to the database. Please try again later.", ephemeral=True)
            return


        collections = ['warn_collection', 'blacklist_collection', 'ban_collection']
        found_cases = []


        # Query each collection
        
        for collection_name in collections:
            
            collection = mongo_db[collection_name]

            
            result = await collection.find_one({"case_number": f"Case #{case_id}"})
            
            
            if result:
                found_cases.append((collection_name, result))
                
                
            else:
                print(f"")


        # If cases are found, send the embed
        
        if found_cases:
            
            for collection_name, result in found_cases:
                
                case_number = result.get('case_number', f"Case #{case_id}")
                action_time = result.get('action_time', datetime.utcnow())
                formatted_time = action_time.strftime('%B %d, %Y %I:%M %p')


                # Determine user and moderator field names based on the collection
                
                if collection_name == "ban_collection":
                    
                    
                    user_id = result.get('banned_user_id', 'N/A')
                    user_name = result.get('banned_user_name', 'N/A')
                    mod_id = result.get('banned_by_id', 'N/A')
                    mod_name = result.get('banned_by_name', 'N/A')
                    
                    
                elif collection_name == "blacklist_collection":
                    
                    
                    user_id = result.get('blacklisted_user_id', 'N/A')
                    user_name = result.get('blacklisted_user_name', 'N/A')
                    mod_id = result.get('blacklisted_by_id', 'N/A')
                    mod_name = result.get('blacklisted_by_name', 'N/A')
                    
                    
                else:
                    
                    
                    user_id = result.get('user_id', 'N/A')
                    user_name = result.get('user_name', 'N/A')
                    mod_id = result.get('moderator_id', 'N/A')
                    mod_name = result.get('moderator_name', 'N/A')


                # Format user and moderator mentions
                
                user_mention = f"<@{user_id}> ({user_id})" if user_id != 'N/A' else user_name
                mod_mention = f"<@{mod_id}> ({mod_id})" if mod_id != 'N/A' else mod_name


                reason = result.get('reason', 'No reason provided')


                # Create the embed
                
                embed = discord.Embed(title=f"{collection_name.capitalize()} | {case_number}",
                                    description=f"Action took place on {formatted_time}!",
                                    color=constants.merx_embed_color_setup())
                
                
                embed.add_field(name="Member", value=user_mention, inline=True)
                embed.add_field(name="Moderator", value=mod_mention, inline=True)
                embed.add_field(name="Reason", value=reason, inline=False)
                

                # Send the embed
                
                await ctx.send(embed=embed)
                
                
        else:
            await ctx.send(f"<:xmark:1285350796841582612> No case found with case ID {case_id}.")



async def setup(merx):
    await merx.add_cog(CaseSearchCog(merx))
