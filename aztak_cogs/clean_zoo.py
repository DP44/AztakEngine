import asyncio
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

# --------------------------------------------------------------------------
# COG:          An automated task to clean the #zoo channel.
# --------------------------------------------------------------------------
class CleanZoo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Start our task.
        self.clean_zoo.start()

    def cog_unload(self):
        self.clean_zoo.cancel()

    async def get_message_count(self, channel):
        count = 0

        # count all the messages.
        async for message in channel.history(limit=None):
            count += 1

        return count

    def check_message(self, message):
        # delete bot messages.
        if type(message.author) == discord.User:
            return False

        # Get the little torture creature role.
        creature_role = discord.utils.get(message.author.guild.roles, 
                                          id=826243626560520234)

        # We don't want to delete messages from our little torture slaves.
        if not creature_role in message.author.roles:
            return True

        # Not a creature, could easily have some no no stuff, so we delete.
        return False

    @tasks.loop(hours=24.0)
    async def clean_zoo(self):
        bf.log("cleaning #zoo.", level=1)

        # Get the zoo channel.
        zoo = self.bot.get_channel(838085979784871936)

        message_count = await self.get_message_count(zoo)

        deleted_messages = await zoo.purge(limit=message_count, 
                                           check=self.check_message)

    @clean_zoo.before_loop
    async def before_cleanzoo(self):
        print('\nCleanZoo loaded.\n')

        # Make sure the bot is ready before running the loop.
        await self.bot.wait_until_ready()
