import os
import sys
import json
import struct
import logging
import requests
import subprocess
import discord.utils
from datetime import datetime
from base64 import b64decode, b64encode

# Set our config for logging to a file.
logging.basicConfig(filename='aztak.log',
                    filemode='w',
                    # stream=sys.stdout,
                    format='%(asctime)s - (%(levelname)s) => %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# --------------------------------------------------------------------------
# DESCRIPTION:  Logs a message and writes it to aztak.log.
#
#               NOTSET -> 0 or 0
#               DEBUG -> 10 or 1
#               INFO -> 20 or 2
#               WARNING -> 30 or 3
#               ERROR -> 40 or 4
#               CRITICAL -> 50 or 5
#
# INPUT:        message         -> The message to log.
#
#               level           -> The level to log as. See above chart, 
#                                  either a single or double digit int is 
#                                  accepted. Defaults to error
#
#               crashmsg        -> The message to show when something fatal
#                                  Happens.
# --------------------------------------------------------------------------
def log(message, level=40, 
        crashmsg='Bot has encountered a fatal error, check logfile.'):
    if level in [4, 40]:
        logging.error(message, exc_info=True)
    
    if level in [5, 50]:
        logging.critical(message, exc_info=True)
        print(f'{crashmsg} Check aztak.log for traceback info.')
        exit()
    else:
        logging.log(level, message)

# --------------------------------------------------------------------------
# DESCRIPTION:  Creates a text box.
#
# INPUT:        title           -> The title of the box.
#
#               content         -> The contents of the box.
# --------------------------------------------------------------------------
def box(title, content):
    # TODO: Clean this up.
    # TODO: Word wrapping.
    title = title.upper()
    max_width = max([len(x) for x in content.split('\n') if x] + [len(title)])
    max_width = 20 if max_width < 20 else max_width
    padding = (max_width - len(title)) // 2
    box_str = f"┌{''.join(['─' for _ in range(max_width + 2)])}┐\n"
    box_str += f"│ {''.join([' ' for _ in range(padding)])}{title}{''.join([' ' for _ in range(padding)])}  │\n"
    box_str += f"│ {''.join([' ' for _ in range(max_width)])} │\n"

    for line_num, line in enumerate([x for x in content.split('\n') if x]):
        box_str += f"│ {line}{''.join([' ' for _ in range(max_width - len(line))])} │\n"

    box_str += f"└{''.join(['─' for _ in range(max_width + 2)])}┘"

    split = box_str.split('\n')

    if len(split[0]) < len(split[1]):
        split[1] = f"│ {''.join([' ' for _ in range(padding)])}{title}{''.join([' ' for _ in range(padding - 1)])}  │"
        box_str = '\n'.join(split)

    return box_str

# --------------------------------------------------------------------------
# DESCRIPTION:  Uploads the given content to a service.
#
# INPUT:        content         -> The content to upload.
# --------------------------------------------------------------------------
def content_upload(content):
    response = requests.post('http://ix.io', files={ 
        'f:1': ('file.ext', content.encode()) 
    })

    return response.text

# --------------------------------------------------------------------------
# DESCRIPTION:  Gets info on a certain specified drug. (Why?)
#
# INPUT:        drug            -> The drug to look up.
# --------------------------------------------------------------------------
def info(drug):
    # TODO: Word wrapping.
    endpoint = "http://tripbot.tripsit.me/api/tripsit/getDrug?name="
    query = requests.get(f"{endpoint}{drug.lower()}").json()

    if query['err']:
       return box("Error", f'No drug "{drug}" found.')
    else:
        body = query['data'][0]
        name = body['name']
        summary = body['properties']['summary'].split('. ')[0]

        try:
            dose = body['properties']['dose'].split(' | ')

            # yeah, yeah I fuckin know
            formatted_doses = {
                roa.split(' ')[0]:[f"{x[1]} ({x[0].replace(':', '')})" for x in [(roa.replace(roa.split(' ')[0], '').strip().replace(':', '').split(' ')[i], roa.replace(roa.split(' ')[0], '').strip().replace(':', '').split(' ')[i + 1]) for i in range(0, len(roa.replace(roa.split(' ')[0], '').strip().replace(':', '').split(' ')), 2)]] for roa in dose if roa.split(' ')[0] != "Note:"
            }
           
            duration = body['properties']['duration'].split(' | ')
            onset = [f'{x[0]}: {x[1]}' for x in [x.split(': ') for x in body['properties']['onset'].split(' | ')]]
            dose_str = [f"{x}: {', '.join(formatted_doses[x])}" for x in formatted_doses]
            dose_box = box("Doses", '\n'.join(dose_str))
            duration_box = box("Duration", '\n'.join(duration))
            onset_box = box("Onset", '\n'.join(onset))
            msg = f"Summary: {summary}\n{dose_box}\n" + \
                  f"{duration_box}\n{onset_box}"
            return box(f"{name} info", msg)
        except Exception:
            return box(f"{name} info", json.dumps(body['properties'], 
                       indent=3))

# --------------------------------------------------------------------------
# DESCRIPTION:  Uses an API to handle crypto exchanges.
#
# INPUT:        value           -> The current crypto amount.
#
#               current_type    -> Current currency to compare.
#
#               target_type     -> Target currency to compare.
# --------------------------------------------------------------------------
def crypto(value, current_type, target_type):
    valid = [
        'ETH', 'BTC', 'XMR', 'LTC', 'BCH', 
        'EOS', 'USD', 'GBP', 'JPY', 'EUR', 'CAD'
    ]

    if current_type.upper() not in valid or \
       target_type.upper() not in valid:
        return f"Invalid currency type. Supported: {', '.join(valid)}"

    # TODO: Put this somewhere safe.
    token = open(".crypto_token", 'r').read()
    rsp = requests.get(f"https://min-api.cryptocompare.com/data/price?" + 
                       f"fsym={current_type}&tsyms={target_type}&" + 
                       f"api_key={token}").json()
    return box(f"{current_type.upper()} TO {target_type.upper()}", 
               f"{current_type.upper()}: {value}\n" + 
               f"{target_type.upper()}: " + 
               f"{float(value) * float(rsp[target_type.upper()])}")

# --------------------------------------------------------------------------
# DESCRIPTION:  Checks if the process is ran as root.
# --------------------------------------------------------------------------
def is_admin():
    return os.getuid() == 0

# --------------------------------------------------------------------------
# DESCRIPTION:  Checks if the grabify nuker is already running.
# --------------------------------------------------------------------------
def is_grabify_nuker_running():
    procs = subprocess.check_output("ps aux | grep grabify-nuke.py", 
                                    shell=True).decode().split('\n')
    
    for proc in procs:
        if "python3 /home/ec2-user/AztakEngine/grabify-nuke.py" in proc:
            return True

    return False

# --------------------------------------------------------------------------
# DESCRIPTION:  Returns the PID of the active nuker instance.
# --------------------------------------------------------------------------
def get_nuker_pid():
    procs = subprocess.check_output("ps aux | grep grabify-nuke.py", 
                                    shell=True).decode().split('\n')
   
    nuker_proc = ""

    proc_names = [
        "python3 /home/ec2-user/AztakEngine/grabify-nuke.py",
    ]

    for proc in procs:
        # There's probably a cleaner way of doing this, but this 
        # is the only way i know of checking for multiple strings.
        for name in proc_names:
            if name in proc:
                nuker_proc = proc
                break

    # If we find an empty string then that 
    # means there's no active nuker instances.
    if nuker_proc == "":
        return ""

    proc_data = nuker_proc.split(" ")

    # Iterate from end of list.
    for i in range(len(proc_data) - 1, -1, -1):
        # Remove any empty entries in proc_data.
        if proc_data[i] == "":
            proc_data.pop(i)

    # Return the second entry of the list as that is our process ID.
    return proc_data[1]

# --------------------------------------------------------------------------
# DESCRIPTION:  Runs the grabify nuker.
#
# INPUT:        url             -> The url to flood.
# --------------------------------------------------------------------------
def run_grabify_nuker(url):
    # Start a new process.
    subprocess.Popen(
        f"python3 /home/ec2-user/AztakEngine/grabify-nuke.py {url} &", 
        shell=True
    )

# --------------------------------------------------------------------------
# DESCRIPTION:  Kills the active grabify instance.
# --------------------------------------------------------------------------
def kill_grabify_instance():
    # Get the PID for the active nuker instance.
    nuker_pid = get_nuker_pid()

    if nuker_pid != "":
        subprocess.Popen(f"kill {nuker_pid}", shell=True)

# --------------------------------------------------------------------------
# DESCRIPTION:  Combine bytestrings from a bytearray.
# 
# INPUT:        array           -> The array to combine.
# --------------------------------------------------------------------------
def combine_bytestrings(array):
    # TODO: Replace combine_bytestrings by using extend method
    combined = bytearray()

    for x in array:
        combined.extend(x)

    return combined

# --------------------------------------------------------------------------
# DESCRIPTION:  Convert data into bytes
#
# INPUT:        data            -> The data to convert.
#
#               flag            -> The struct flag.
#
#               encode          -> Specifies if we should encode or decode.
# --------------------------------------------------------------------------
def byte_conversion(data, flag, encode=False):
    if encode is False:
        return struct.unpack(flag, data)
    else:
        return bytearray(struct.pack(flag, data))

# --------------------------------------------------------------------------
# DESCRIPTION:  Convert bytearray to a hexstring.
#                       
# INPUT:        bytearr         -> The byte array to convert.
# --------------------------------------------------------------------------
def bytearr_to_hexstring(bytearr):
    return ''.join(
        [f"\\0x{code}" for code in [f'{i:0>2X}' for i in bytearr]]
    )[1:]

# --------------------------------------------------------------------------
# DESCRIPTION:  Calculate the CRC checksum of the data specified.
#
# INPUT:        data            -> The data to calculate.
# --------------------------------------------------------------------------
def calculate_crc_checksum(data):
    """
    The checksum is calculated with a CRC-16-CCITT (17 bit) 
    cyclic redundancy check algorithm.

    https://en.wikipedia.org/wiki/Cyclic_redundancy_check
    ------------------------------------------------------------------------
    Here is a basic explanation of how CRCs are computed. To 
    compute an n-bit binary CRC, line the bits representing 
    the input in a row, and position the (n + 1)-bit pattern 
    representing the CRC's divisor (called a "polynomial")
    underneath the left-hand end of the row... The polynomial 
    is written in binary as the coefficients
    ------------------------------------------------------------------------

    This function takes a block of data and returns a two byte checksum for 
    it
    """
    data = bytearray([x for x in data])
    high_order, low_order = 0xFF, 0xFF

    for i in range(0, len(data)):
        current_byte = data[i] ^ high_order
        current_byte ^= (current_byte >> 4)
        high_order = (low_order ^ (current_byte >> 3) ^ 
                                  (current_byte << 4)) & 255
        low_order = (current_byte ^ (current_byte << 5)) & 255

    full_checksum = byte_conversion(high_order << 8 | low_order, 'H', 
                                    encode=True)
    return full_checksum

# --------------------------------------------------------------------------
# DESCRIPTION:  Base64 encode or decode a string.
#
# INPUT:        string          -> The string to encode or decode.
#
#               decode          -> Specifies if we should encode or decode.
# --------------------------------------------------------------------------
def base64(string, decode=True):
    return b64decode(string) if decode else b64encode(string)

# --------------------------------------------------------------------------
# DESCRIPTION:  Check if a message should be purged from zoo.
#
# INPUT:        message         -> The message object to check.
# --------------------------------------------------------------------------
def check_message(message):
    # Delete bot messages.
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

# --------------------------------------------------------------------------
# DESCRIPTION:  Returns the message count in a specific channel.
#
# INPUT:        channel         -> The channel to check.
# --------------------------------------------------------------------------
async def get_message_count(channel):
    count = 0

    # count all the messages.
    async for message in channel.history(limit=None):
        count += 1

    return count

# --------------------------------------------------------------------------
# DESCRIPTION:  Check the type of a given string.
#
# INPUT:        string          -> The string to check.
# --------------------------------------------------------------------------
def check_type(string):
    if string.lower() in ['true', 'false']:
        return 'bool'

    try:
        float(string)

        if '.' in string:
            return 'float'
    except Exception:
        pass

    try:
        int(string)

        if '.' in string:
            return 'float'
        else:
            return 'int'
    except Exception:
        pass

    if isinstance(string, str):
        if len(string) == 1:
            return 'char'
        else:
            return 'str'

# --------------------------------------------------------------------------
# DESCRIPTION:  Get a DNS record from a specified address.
#
# INPUT:        addr            -> The address to check.
#
#               record          -> The record to check.
# --------------------------------------------------------------------------
def get_records(addr, record):
    return json.dumps(requests.get(
        f"https://dns.google.com/resolve?name={addr}&type={record.upper()}"
    ).json(), indent=3)

# --------------------------------------------------------------------------
# DESCRIPTION:  Get info based off an ip address.
#
# INPUT:        addr            -> The address to check.
#
#               fields          -> The fields to get.
# --------------------------------------------------------------------------
def get_address_info(addr, 
                     fields="country,countryCode,isp,org,as,mobile,proxy"):
    # AVAILABLE OPTIONS: status, message, continent, continentCode, country, 
    #                    countryCode, region, regionName, city, district, 
    #                    zip, lat, lon, timezone, offset, currency, isp, 
    #                    org, as, asname, reverse, mobile, proxy, hosting, 
    #                    query.

    # Get the address info.
    results = requests.get(
        f"http://ip-api.com/line/{addr}?fields=status,message," + 
        f"{fields},query"
    ).text.split("\n")

    # remove the last element as there's a newline that's empty.
    results.pop()

    # return our results.
    return results

# --------------------------------------------------------------------------
# DESCRIPTION:  Calculate Account Age From User ID
#
# INPUT:        uid            -> The User ID
# --------------------------------------------------------------------------
def calculate_account_age(uid):
    duration = datetime.now() - datetime.fromtimestamp(
        ((uid >> 22) + 1420070400000) / 1000
        )

    total_seconds = duration.total_seconds()
    
    year = divmod(total_seconds, 31536000)
    day = divmod(year[1] if year[1] is not None else total_seconds, 86400)
    hour = divmod(day[1] if day[1] is not None else total_seconds, 3600)
    minute = divmod(hour[1] if hour[1] is not None else total_seconds, 60)
    second = \
        divmod(minute[1], 1) if minute[1] is not None else total_seconds
   
    return f"{int(year[0])} years, {int(day[0])} days, " + \
           f"{int(hour[0])} hours, {int(minute[0])} minutes, " + \
           f"and {int(second[0])} seconds"


# TODO: Implement urlscan.io API
# NOTE: The urlscan.io API key can be found in .urlscan_api_key
