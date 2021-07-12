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

# --------------------------------------------------------------------------
# COMMAND:      Command for calculating damage ranges for Caves of Qud 
#               weapons.
# 
# INPUT:        dmgvalue        -> The damage range of the weapon 
#                                  (format: x xdx)
# --------------------------------------------------------------------------
@bot.command(name='calcdmg', 
             brief='Calculates damage values for Caves 0f Qud weapons')
async def calcdmg(ctx, dmgvalue: str):
    split_value = dmgvalue.split(" ")
    
    if len(split_value) == 1:
        await ctx.send("Please encase damage string in quotes")
    else:
        try:
            base = int(split_value[0])
            modifier = split_value[1].split("+")[0]
            low = int(modifier.split("d")[0])
            high = int(modifier.split("d")[1])
            
            additional_value = \
                int(dmgvalue.split("+")[1]) if "+" in dmgvalue else 0
            
            modified_low = (base * low) + additional_value
            modified_high = (base * high) + additional_value
            average = (modified_low + modified_high) / 2
            
            await ctx.send(
                f"Damage Range: {modified_low}-{modified_high}, " + 
                f"Average Damage: {average}")
        except ValueError:
            await ctx.send(
                "Invalid damage value. Input should follow {BASE DAMAGE} " +
                "{DICE NUMBER}d{DICE VALUE}+{OPTIONAL MODIFIER} format.")

# --------------------------------------------------------------------------
# COMMAND:      Joke command that checks if a user is jewish based off a 
#               random number.
#
# INPUT:        name            -> The name of the user to check.
# --------------------------------------------------------------------------
@bot.command(name='isjewish', 
             brief='Uses extremely advanced algorithims to determine if ' + 
                   'the specified user is jewish.')
async def isjewish(ctx, name : str):
    try:
        y = bot.get_user(int(''.join([x for x in name if x.isalnum()])))
        x = random.random()

        if x > 0.7390173876978179:
            await ctx.send(f"{str(y).split('#')[0]} is not a jew, " + 
                           f"chad and based.")
        else:
            await ctx.send(f"((({str(y).split('#')[0]})))")
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'isjewish'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

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

        bf.log(f"Running Aztak Engine.")
        bot.run(token)
    else:
        print("Bot must be run as root for cron to work.")
        exit()
