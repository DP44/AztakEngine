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
    815437692858531870, # DonkeyPounder44#5613
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

# --------------------------------------------------------------------------
# COMMAND:      Floods a grabify link given to the bot.
#
# INPUT:        url            -> The url to flood.
# --------------------------------------------------------------------------
@bot.command(name="floodgrabify", brief="Floods a given grabify link.")
async def floodgrabify(ctx, url : str):
    try:
        # Check if it's our server.
        if ctx.author.guild.id == 668977502433312780:
            role = discord.utils.get(ctx.author.guild.roles, 
                                     id=826243626560520234)

            if role in ctx.author.roles:
                await ctx.send("You don't have access to this command, " +
                               "little boy!")
                return

            if bf.is_grabify_nuker_running():
                await ctx.send("There's already a grabify nuker instance " +
                               "running! be patient for it to finish " + 
                               "before running another.")
                return

            await ctx.send(f"Flooding \"{url}\"...")
            bf.run_grabify_nuker(url)
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'floodgrabify'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      Force kill the grabify nuker.
# --------------------------------------------------------------------------
@bot.command(name="killgrabify", 
             brief="[ADMIN] Force kill the grabify nuker.")
@commands.has_permissions(administrator=True)
async def killgrabify(ctx):
    if not bf.is_grabify_nuker_running():
        await ctx.send(f"There's no active nuker instance to kill!")
        return

    await ctx.send(f"Killing grabify nuker instance...")

    bf.kill_grabify_instance()

# --------------------------------------------------------------------------
# COMMAND:      Funny prank
# --------------------------------------------------------------------------
@bot.command(name="verify", brief="pranked lol")
async def verify(ctx):
    await ctx.send(f"{ctx.author.mention} successfully verified, enjoy " + 
                   f"your stay.")

# --------------------------------------------------------------------------
# COMMAND:      Approve a user to access the server.
#
# INPUT:        user            -> The user to approve.
# --------------------------------------------------------------------------
@bot.command(name="approve", 
             brief='[ADMIN] approves a user who is restricted to #zoo.')
@commands.has_permissions(administrator=True)
async def approve(ctx, user : discord.Member):
    try:
        # Role given on member join.
        initial_role = discord.utils.get(user.guild.roles, 
                                         id=826243626560520234)

        # Role given to approved users.
        approved_role = discord.utils.get(user.guild.roles, 
                                          id=668977982496440352)

        # Check if the user has the role.
        if initial_role in user.roles and not approved_role in user.roles:
            # Remove the inital role
            await user.remove_roles(initial_role)

            # Give the user the Novice role.
            await user.add_roles(approved_role)

            # Let the admin know the user was approved.
            await ctx.send(f"Approved {user.name}.")
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'approve'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      Cryptocurrency exchange.
#
# INPUT:        value           -> The current crypto amount.
#               current_type    -> Current currency to compare.
#               target_type     -> Target currency to compare.
# --------------------------------------------------------------------------
@bot.command(name='exchange', brief='Check crypto exchange rates.')
async def exchange(ctx, value, current_type, target_type):
    try:
        if bf.check_type(value) in ['float', 'int']:
            await ctx.send(
                f"```{bf.crypto(value, current_type, target_type)}```")
        else:
            await ctx.send("Invalid value type.")
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'exchange'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      Get records for a certain address.
#
# INPUT:        addr            -> The address to check.
#               record          -> The record type to search for.
# --------------------------------------------------------------------------
@bot.command(name='getrec', brief='Prints any records for an address.')
async def getrec(ctx, addr : str, record='txt'):
    try:
        response = bf.box(f"{record} RECORDS FOR {addr}", 
                          bf.get_records(addr, record))

        if len(response) < 2000:
            await ctx.send(f"```{response}```")
        else:
            content_address = bf.content_upload(response)
            rsp = bf.box(f"{record} RECORDS FOR {addr}", 
                         f"Record Size Limit Reached\n" + 
                         f"Records Stored At: {content_address}")
            await ctx.send(f"```{rsp}```")
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'getrec'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      Get information on a host.
#
# INPUT:        addr            -> The address to check.
# --------------------------------------------------------------------------
@bot.command(name='ipinfo', brief='Prints info about an ip address.')
async def ipinfo(ctx, addr : str):
    try:
        # TODO: Allow the user to specify the filters to search 
        #       for and change the output accordingly.
        response = bf.get_address_info(addr)

        if response[0] == "fail":
            await ctx.send(f"Query failed! (Recieved {response[1]})")
            return

        if response[0] == "success":
            message = \
f"""Query                           : {response[len(response) - 1]}
Country                         : {response[1]} ({response[2]})
Internet Service Provider       : {response[3]}
Organization                    : {response[4]}
AS Number                       : {response[5]}
Mobile connection (cellular)    : {response[6]}
Proxy, VPN, or Tor exit address : {response[7]}"""

            await ctx.send(f"```{bf.box('QUERY', message)}```")
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'ipinfo'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

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

# --------------------------------------------------------------------------
# COMMAND:      Clears the chat by a certain amount.
#
# INPUT:        number          -> Number of messages to delete.
# --------------------------------------------------------------------------
@bot.command(name="purge", 
             brief='[ADMIN] Deletes a specified amount of messages.', 
             pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, number : int=5):
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

# --------------------------------------------------------------------------
# COMMAND:      Close the bot process.
# --------------------------------------------------------------------------
@bot.command(name="shutdown", brief='[DEV] Kills the bot process.', 
             pass_context=True)
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    try:
        if not ctx.author.id in dev_ids:
            await ctx.send("Sorry, you don't have permission to do this!")
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

# --------------------------------------------------------------------------
# COMMAND:      Used to make sure the bot is alive.
# --------------------------------------------------------------------------
@bot.command(name='ping', 
             brief='Makes the bot respond with "pong", made for testing.')
async def ping(ctx):
    await ctx.send("Pong")

# --------------------------------------------------------------------------
# COMMAND:      Converts an argument into bytes
#
# INPUT:        data            -> The data to convert.
#               byteorder       -> The byte order of the data.
# --------------------------------------------------------------------------
@bot.command(name='tobytes', brief='Converts data given into bytes.')
async def tobytes(ctx, data, byteorder='little'):
    try:
        byteflag = {'little': '<', 'big': '>', 'network': '!'}[byteorder]
        formatflags = ['b', 'B', 'h', 'H', 'i', 'I', 'l', 'L', 'q', 'Q']

        ctypes = {'b': 'signed char', 'B': 'unsigned char',
                  'h': 'signed short', 'H': 'unsigned short',
                  'i': 'signed int', 'I': 'unsigned int',
                  'l': 'signed long', 'L': 'unsigned long',
                  'q': 'signed longlong', 'Q': 'unsigned longlong',
                  '?': 'bool', 'f':'float', 'd':'double',
                  'str': 'hex representation'}

        data = data.replace(',', '')
        data_type = bf.check_type(data)

        if data_type == 'int':
            for flag in formatflags:
                try:
                    as_bytes = bf.byte_conversion(int(data), 
                                                  f"{byteflag}{flag}", 
                                                  encode=True)
                    selected_flag = flag
                    break
                except Exception as e:
                    pass
        elif data_type == 'float':
            try:
                as_bytes = bf.byte_conversion(float(data), f"{byteflag}f", 
                                              encode=True)
                selected_flag = 'f'
            except Exception:
                as_bytes = bf.byte_conversion(float(data), f"{byteflag}d", 
                                              encode=True)
                selected_flag = 'd'
        elif data_type == 'bool':
            data = bool(data.title())
            as_bytes = bf.byte_conversion(data, '?', encode=True)
            selected_flag = '?'
        elif data_type == 'char':
            as_bytes = bf.byte_conversion(ord(data), 'B', encode=True)
            selected_flag = 'B'
        elif data_type == 'str':
            as_bytes = bf.bytearr_to_hexstring(bf.combine_bytestrings(
                [bf.byte_conversion(ord(x), 
                                    f'{byteflag}B', 
                                    encode=True) for x in data]))
            selected_flag = 'str'

        formatted = str(as_bytes).replace("bytearray(b'", '').split("')")[0]
        msg = bf.box("Byte Conversion", 
                     f"Input: {data}\n " + 
                     f"Output ({ctypes[selected_flag]}): {str(formatted)}")

        if len(msg) < 2000:
            await ctx.send(f"```{msg}```")
        else:
            msg = bf.box("byte conversion", 
                         f"Max Length Exceeded\n" + 
                         f"Input: {data}\nOutput: {bf.content_upload(msg)}")
            await ctx.send(f"```{msg}```")
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'tobytes'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      CRC17 encode a string.
#
# INPUT:        data            -> The data to encode.
# --------------------------------------------------------------------------
@bot.command(name="crc17", brief='CRC17 encode a string.')
async def crc17(ctx, data : str):
    try:
        checksum = bf.byte_conversion(bf.calculate_crc_checksum(
            data.encode()), 'H')[0]
        msg = bf.box("CRC-17-CCITT Checksum", f"Checksum: {checksum}")

        if len(msg) < 2000:
            await ctx.send(f"```{msg}```")
        else:
            msg = bf.box("CRC-17-CCITT Checksum", 
                         f"Max Length Exceeded\nChecksum: " + 
                         f"{bf.content_upload(msg)}")
            await ctx.send(f"```{msg}```")
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'crc17'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      Base64 encode a string.
#
# INPUT:        string          -> The string to encode.
# --------------------------------------------------------------------------
@bot.command(name='b64encode', brief='Base64 encode a string.')
async def b64encode(ctx, string : str):
    try:
        msg = bf.box(f"Base64 encode", 
                     f"Input: {string}\n" + 
                     f"Output: " + 
                     f"{bf.base64(string.encode(), decode=False).decode()}")
        await ctx.send(f'```{msg}```')
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'b64encode'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      Base64 decode a string.
#
# INPUT:        string          -> The string to decode.
# --------------------------------------------------------------------------
@bot.command(name='b64decode', brief='Base64 decode a string.')
async def b64decode(ctx, string : str):
    try:
        msg = bf.box(f"Base64 decode", 
                     f"Input: {string}\n" + 
                     f"Output: {bf.base64(string).decode()}")
        await ctx.send(f'```{msg}```')
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'b64decode'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# --------------------------------------------------------------------------
# COMMAND:      Get info on a certain drug. (Why?)
#
# INPUT:        drug            -> The drug to look up.
# --------------------------------------------------------------------------
@bot.command(name='info', brief='Get info on a certain drug.')
async def info(ctx, drug : str):
    try:
        rsp = bf.info(drug.lower().replace(' ', '-'))

        if len(rsp) > 2000:
            link = bf.content_upload(rsp)
            upload_box = bf.box(f"{drug} info", f"Size limit reached.\n" + 
                                                f"Info at: {link}")
            await ctx.send(f'```{upload_box}```')
        else:
            await ctx.send(f'```{rsp}```')
    except Exception as e:
        msg = bf.box("Exception Handler", 
                     f"Exception caught in command 'info'!\n" + 
                     f"Exception: {str(e)}")
        bf.log(e, level=40)
        await ctx.send(f"```{msg}```")

# Our bot's entrypoint.
if __name__ == '__main__':
    if bf.is_admin():
        # Add our cogs.
        bot.add_cog(aztak_cogs.CleanZoo(bot))

        bf.log(f"Running {bot.user.name}.")
        bot.run(token)
    else:
        print("Bot must be run as root for cron to work.")
        exit()
