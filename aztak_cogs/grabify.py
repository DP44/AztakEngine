import asyncio
import requests
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling the grabify flooder.
# --------------------------------------------------------------------------
class Grabify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------
    # COMMAND:      Floods a grabify link given to the bot.
    #
    # INPUT:        url            -> The url to flood.
    # ----------------------------------------------------------------------
    @commands.command(name="floodgrabify", 
                      brief="Floods a given grabify link.")
    async def floodgrabify(self, ctx, url: str):
        try:
            # Check if it's our server.
            if ctx.author.guild.id == 668977502433312780:
                role = discord.utils.get(ctx.author.guild.roles, 
                                         id=826243626560520234)

                if role in ctx.author.roles:
                    await ctx.send("You don't have access to this " + 
                                   "command, little boy!")
                    return

                if bf.is_grabify_nuker_running():
                    await ctx.send("There's already a grabify nuker " + 
                                   "instance running! be patient for it " + 
                                   "to finish before running another.")
                    return

                await ctx.send(f"Flooding \"{url}\"...")
                bf.run_grabify_nuker(url)
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'floodgrabify'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")

    # ----------------------------------------------------------------------
    # COMMAND:      Force kill the grabify nuker.
    # ----------------------------------------------------------------------
    @commands.command(name="killgrabify", 
                      brief="[ADMIN] Force kill the grabify nuker.")
    @commands.has_permissions(administrator=True)
    async def killgrabify(self, ctx):
        if not bf.is_grabify_nuker_running():
            await ctx.send(f"There's no active nuker instance to kill!")
            return

        await ctx.send(f"Killing grabify nuker instance...")

        bf.kill_grabify_instance()
