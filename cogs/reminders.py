import discord
import uuid
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from utils.embeds import ReminderEmbed
from utils.constants import MerxConstants, reminders
 


constants = MerxConstants()

class ReminderCommandsCog(commands.Cog):
    def __init__(self, merx):
        self.merx = merx
        self.mongo_db = None
        self.check_for_reminders.start()


    
    @tasks.loop(minutes=1)
    async def check_for_reminders(self):
        async for reminder in reminders.find({}):
            if reminder["time"] == datetime.now().strftime('%Y-%m-%d %H:%M'):
                print("Reminder went off.")
                await self.merx.get_user(reminder["user_id"]).send("Your reminder went off :)")
                reminders.delete_one(reminder)
        



    @commands.hybrid_command(description="This will create a reminder.", with_app_command=True, extras={"category": "General"})
    async def addreminder(self, ctx: commands.Context, name:str, time:str, message:str):
        try:
            newtime = self.time_converter(datetime.now().strftime('%Y-%m-%d %H:%M'),time)
        except ValueError:
            return await ctx.send(embed=discord.Embed(
                title="Invalid time",
                description="You provided a invalid time.",
                color=discord.Color.red()
            ))

        
        data = {
            "id": str(uuid.uuid4().int)[:4],
            "user_id": ctx.author.id,
            "name": name,
            "message": message,
            "time": newtime
        }

        reminders.insert_one(data)

        reminder_embed = ReminderEmbed(reminder_time=newtime)

        await ctx.send(embed=reminder_embed)
        
    

    def time_converter(self, current_date: str, parameter: str) -> int:
        conversions = {
            ("s", "seconds"): 1,
            ("m", "minutes"): 60,
            ("h", "hours"): 60 * 60,
            ("d", "days"): 24 * 60 * 60,
            ("w", "weeks"): 7 * 24 * 60 * 60
        }

        current_date = datetime.strptime(current_date, '%Y-%m-%d %H:%M')
        parameter = parameter.strip()
        
        for aliases, multiplier in conversions.items():
            for alias in aliases:
                if parameter.lower().endswith(alias.lower()):
                    number_part = parameter[:-len(alias)].strip()
                    
                    if number_part.isdigit():
                        time_to_add = int(number_part) * multiplier
                        new_date = current_date + timedelta(seconds=time_to_add)
                        return new_date.strftime('%Y-%m-%d %H:%M')
                    else:
                        raise ValueError(f"Invalid number: {number_part}")

        raise ValueError(f"Invalid time format: {parameter}")



async def setup(merx):
    await merx.add_cog(ReminderCommandsCog(merx))