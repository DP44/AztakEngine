import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

# --------------------------------------------------------------------------
# COG:          An automated task to clean the #soldiers channel of any sin.
# --------------------------------------------------------------------------
class CleanSoldiers(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		# Start our task.
		self.clean_soldiers.start()

	def cog_unload(self):
		self.clean_soldiers.cancel()

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

		# Don't delete the message if it's a pinned message.
		if message.pinned:
			return True

		# TODO: Only delete messages with stuff that can cause future problems.

		return False

	@tasks.loop(hours=24.0)
	async def clean_soldiers(self):
		# Get the soldiers channel.
		soldiers = self.bot.get_channel(924446555904286760)

		bf.log("cleaning #soldiers.")

		# Purge collected messages.
		deleted_messages = await soldiers.purge(check=self.check_message,
												oldest_first=True)

	@clean_soldiers.before_loop
	async def before_cleansoldiers(self):
		print('\nCleanSoldiers loaded.\n')

		# Make sure the bot is ready before running the loop.
		await self.bot.wait_until_ready()
