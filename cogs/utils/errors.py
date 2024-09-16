import discord
from discord import Interaction
from cogs.utils.embeds import SuccessEmbed, ErrorEmbed

# This is the errors file. This first part sends an error to the user with an error code and a link to get support

async def send_error_embed(interaction: Interaction, error: Exception, error_id: str):
    
    embed = ErrorEmbed(error=error, error_id=error_id)
    
    
    # Send the embed as a follow-up message
    
    if not interaction.response.is_done():
        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:    
        await interaction.followup.send(embed=embed, ephemeral=False)


