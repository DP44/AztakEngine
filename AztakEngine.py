#!/usr/bin/env python3
import random
import discord.utils
import bot_functions as bf
from discord.ext import commands

# Import our cogs.
import aztak_cogs

# Get our bot's token.
token = open(".token", 'r').read()

# Specify the bot intents.
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

# List of user IDS for the devs.
dev_ids = [
    665755257460097064, # Mili#0001
    856607025369841664, # DonkeyPounder44#3091
]

# --------------------------------------------------------------------------
# EVENT:        Called when the bot is ready.
# --------------------------------------------------------------------------
@bot.event
async def on_ready():
    # Let us know that it's ready.
    print(f'{bot.user.name} Is Activated.')

# --------------------------------------------------------------------------
# EVENT:        Called when a member joins a server.
#
# INPUT:        member          -> The member class of the user that joined.
# --------------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    # Check if it's our server.
    if member.guild.id == 668977502433312780:
        try:
            # Get the "Little Torture Creature" role.
            role = discord.utils.get(member.guild.roles, 
                                     id=826243626560520234)

            # Give the user our role.
            await member.add_roles(role)

            await bot.get_channel(838085979784871936).send(
                f"Welcome {member.mention} " + 
                f"[Age: {bf.calculate_account_age(member.id)}], " + 
                f"do $verify to gain access to the server")
        except Exception as e:
            bf.log(e, level=40)

"""
# --------------------------------------------------------------------------
# COMMAND:      Force clear the zoo channel,
# --------------------------------------------------------------------------
@bot.command(name="cleanzoo", brief="[DEV] Force clean the zoo channel.")
@commands.has_permissions(administrator=True)
async def cleanzoo(ctx):
    try:
        if not ctx.author.id in dev_ids:
            await ctx.send("Sorry, you don't have permission to do this!")
            return

        zoo = bot.get_channel(838085979784871936)
        message_count = await bf.get_message_count(zoo)
        
        deleted_messages = await zoo.purge(limit=message_count, 
                                           check=bf.check_message)
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'cleanzoo'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")
"""

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
        bot.add_cog(aztak_cogs.CleanZoo(bot))
        bot.add_cog(aztak_cogs.IMVU(bot))
        bot.add_cog(aztak_cogs.Administrator(bot))
        bot.add_cog(aztak_cogs.Debug(bot))
        bot.add_cog(aztak_cogs.Cryptography(bot))
        bot.add_cog(aztak_cogs.Deprecated(bot))
        bot.add_cog(aztak_cogs.Grabify(bot))
        bot.add_cog(aztak_cogs.Utilities(bot))
        bot.add_cog(aztak_cogs.Twitch(bot, '.twitch_accounts'))

        bf.log(f"Running Aztak Engine.")
        bot.run(token)
    else:
        print("Bot must be run as root for cron to work.")
        exit()
