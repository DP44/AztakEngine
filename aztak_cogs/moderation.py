import asyncio
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

logger = bf.Logger("Moderation (Cog)", 1)

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling Admin commands.
# --------------------------------------------------------------------------
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        logger.message("Initializing cog: Moderation")

    # ----------------------------------------------------------------------
    # COMMAND:      Clears the chat by a certain amount.
    #
    # INPUT:        number          -> Number of messages to delete.
    # ----------------------------------------------------------------------
    @commands.command(name="purge", 
                 brief='[ADMIN] Deletes a specified amount of messages.', 
                 pass_context=True)
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, number: int=5):
        try:
            # Get the current channel the message was sent in.
            channel = ctx.message.channel

            # Delete messages.
            deleted_messages = await channel.purge(limit=number)
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'purge'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")