import os
import pathlib
import importlib
from discord.ext import commands, tasks


def path_from_extension(extension: str) -> pathlib.Path:
    return pathlib.Path(extension.replace(".", os.sep) + ".py")


class HotReload(commands.Cog):
    """
    Cog for reloading extensions as soon as the file is edited.
    """

    def __init__(self, bot):
        self.bot = bot
        self.hot_reload_loop.start()

    def cog_unload(self):
        self.hot_reload_loop.stop()

    @tasks.loop(seconds=3)
    async def hot_reload_loop(self):
        extensions = list(self.bot.extensions.keys())
        extensions.append("cogs.utils.checks")
        for extension in list(self.bot.extensions.keys()):
            if extension in ["jishaku"]:
                continue
            path = path_from_extension(extension)
            time = os.path.getmtime(path)

            try:
                if self.last_modified_time[extension] == time:
                    continue
            except KeyError:
                self.last_modified_time[extension] = time

            try:
                if extension == "cogs.utils.checks":
                    importlib.reload(checks)
                else:
                    await self.bot.reload_extension(extension)
            except commands.ExtensionNotLoaded:
                continue
            except commands.ExtensionError as e:
                print(f"Couldn't reload extension: {extension}, {e}")
            finally:
                self.last_modified_time[extension] = time

    @hot_reload_loop.before_loop
    async def cache_last_modified_time(self):
        self.last_modified_time = {}
        for extension in self.bot.extensions.keys():
            if extension in ["jishaku"]:
                continue
            path = path_from_extension(extension)
            time = os.path.getmtime(path)
            self.last_modified_time[extension] = time


async def setup(bot):
    cog = HotReload(bot)
    await bot.add_cog(cog)