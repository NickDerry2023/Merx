import discord
import uuid
from discord.ext import commands
from utils.constants import MerxConstants, notes

constants = MerxConstants()

class NoteCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
    
    
    
    @commands.hybrid_command(descriptions="Adds a moderator note to a user.", with_app_command=True, extras={"category": "Moderation"})
    async def add_note(self, ctx: commands.Context, member: discord.Member, reason):        
        note_id = f"Note #{str(uuid.uuid4().int)[:4]}"

        note_entry = {
            "note_id": note_id,
            "guild_id": ctx.guild.id,
            "guild_name": ctx.guild.name,
            "noted_user_id": member.id,
            "noted_user_name": str(member),
            "noted_by_id": ctx.author.id,
            "noted_by_name": str(ctx.author),
            "note": reason,
            "timestamp": ctx.message.created_at.isoformat() 
        }

        notes.insert_one(note_entry)

        await ctx.send(f"<:warning:1285350764595773451> **{note_id}** has been logged for {member}.")



    @commands.hybrid_command(descriptions="Delete a note on a user", with_app_command=True, extras={"category": "Moderation"})
    async def remove_note(self, ctx: commands.Context, id):
        notes.delete_one({"note_id": f"Note #{id}"})

        await ctx.send(f"<:warning:1285350764595773451> **Note #{id}** has been removed.")



    @commands.hybrid_command(descriptions="Search for a note on a user", with_app_command=True, extras={"category": "Moderation"})
    async def lookup_note(self, ctx: commands.Context, id):
        result = await notes.find_one({"note_id": f"Note #{id}"})

        if result:
            user_id = result.get('noted_user_id', 'N/A')
            user_name = result.get('noted_user_name', 'N/A')
            mod_id = result.get('noted_by_id', 'N/A')
            mod_name = result.get('noted_by_name', 'N/A')

            note = result.get('note', 'No note provided')

            embed = discord.Embed(
                title=f"Notes | Note #{id}",
                color=constants.merx_embed_color_setup()
            )

            embed.add_field(name="Member", value=f"<@{user_id}> ({user_id})", inline=True)
            embed.add_field(name="Moderator", value=f"<@{mod_id}> ({mod_id})", inline=True)
            embed.add_field(name="Note", value=note, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:xmark:1285350796841582612> No note found with the ID {id}.")



async def setup(merx):
    await merx.add_cog(NoteCommandsCog(merx))