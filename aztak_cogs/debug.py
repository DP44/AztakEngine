import asyncio
import requests
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

# List of user IDS for the devs.
# TODO: Put this in a separate file made for constants.
dev_ids = [
    665755257460097064, # Mili#0001
    856607025369841664, # DonkeyPounder44#3091
]

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling debug commands.
# --------------------------------------------------------------------------
class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------
    # COMMAND:      Close the bot process.
    # ----------------------------------------------------------------------
    @commands.command(name="shutdown", brief='[DEV] Kills the bot process.', 
                 pass_context=True)
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        try:
            if not ctx.author.id in dev_ids:
                await ctx.send(
                    "Sorry, you don't have permission to do this!")
                return

            await ctx.send("Killing bot process.")

            # Log out of the bot and close all connections.
            await bot.close()
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'shutdown'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")

    # ----------------------------------------------------------------------
    # COMMAND:      Used to make sure the bot is alive.
    # ----------------------------------------------------------------------
    @commands.command(name='ping', brief=
                 'Makes the bot respond with "pong", made for testing.')
    async def ping(self, ctx):
        await ctx.send("Pong")