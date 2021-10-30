#!/usr/bin/env python3
import random
import discord.utils
import bot_functions as bf
from discord.ext import commands

logger = bf.Logger("AztakEngine", 1)

# Import our cogs.
import aztak_cogs

# Get our bot's token.
token = open(".token", 'r').read()

# Specify the bot intents.
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

# --------------------------------------------------------------------------
# EVENT:        Called when the bot is ready.
# --------------------------------------------------------------------------
@bot.event
async def on_ready():
    # Let us know that it's ready.
    logger.success(f'{bot.user.name} Is Activated. (Monke Chan)')

# --------------------------------------------------------------------------
# EVENT:        Called when a member joins a server.
#
# INPUT:        member          -> The member class of the user that joined.
# --------------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    # TODO: Move both this event and the verify command to it's own cog.
    # Check if it's our server.
    try:
        # Get the "Peasant" role.
        role = discord.utils.get(member.guild.roles, 
                                 id=876700700120318045)

        # Give the user our role.
        await member.add_roles(role)
    except Exception as e:
        bf.log(e, level=40)

# --------------------------------------------------------------------------
# COMMAND:      Funny prank
# --------------------------------------------------------------------------
@bot.command(name="verify", brief="pranked lol")
async def verify(ctx):
    await ctx.send(f"{ctx.author.mention} successfully verified, enjoy " + 
                   f"your stay.")

# Our bot's entrypoint.
if __name__ == '__main__':
    if bf.is_admin():
        # Add our cogs.
        bot.add_cog(aztak_cogs.Administrator(bot))
        bot.add_cog(aztak_cogs.Debug(bot))
        bot.add_cog(aztak_cogs.Utilities(bot))

        logger.message(f"Running Aztak Engine.")
        bot.run(token)
    else:
        logger.error("Bot must be run as root for cron to work.")
        exit()
