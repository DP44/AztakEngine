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
def log(message, level=20,
        crashmsg='Bot has encountered a fatal error'):
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
    max_width = max([len(x) \
        for x in content.split('\n') if x] + [len(title)])
    max_width = 20 if max_width < 20 else max_width
    padding = (max_width - len(title)) // 2
    box_str = f"┌{''.join(['─' for _ in range(max_width + 2)])}┐\n"
    box_str += f"│ {''.join([' ' for _ in range(padding)]
        )}{title}{''.join([' ' for _ in range(padding)])}  │\n"
    box_str += f"│ {''.join([' ' for _ in range(max_width)])} │\n"

    for line_num, line in enumerate([x for x in content.split('\n') if x]):
        box_str += f"│ {line}{''.join([' ' \
            for _ in range(max_width - len(line))])} │\n"

    box_str += f"└{''.join(['─' for _ in range(max_width + 2)])}┘"

    split = box_str.split('\n')

    if len(split[0]) < len(split[1]):
        split[1] = f"│ {''.join([' ' for _ in range(padding
            )])}{title}{''.join([' ' for _ in range(padding - 1)])}  │"
        box_str = '\n'.join(split)

    return box_str

# --------------------------------------------------------------------------
# DESCRIPTION:  Checks if the process is ran as root.
# --------------------------------------------------------------------------
def is_admin():
    return os.getuid() == 0

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


# --------------------------------------------------------------------------
# CLASS:        A logger for the bot made for displaying messages in the
#               console.
#
# INPUT:        name           -> The name of the project or class actively
#                                 using the logger.
# --------------------------------------------------------------------------
class Logger(object):    
    """ A class for logging messages to the console. """
    # Ported from the myg0t tool development library with some changes.
    # TODO: Clean this up.
    def __init__(self, name, tab_count):
        super(Logger, self).__init__()
        self.name = name
        self.tabs = ("\t" * tab_count)

    # ----------------------------------------------------------------------
    # DESCRIPTION:  Prints a message made to display a successful operation.
    #
    # INPUT:        msg            -> The message to print.
    # ----------------------------------------------------------------------
    def success(self, msg):
        log(f'[{self.name}]{self.tabs}[SUCCESS] {msg}', 2)

        print(f"\x1B[90m[\x1B[93m{self.name}\x1B[90m]{self.tabs}" + \
              f"[\x1B[32mSUCCESS\x1B[90m]\x1B[0m {msg}")

    # ----------------------------------------------------------------------
    # DESCRIPTION:  Prints a message made to display general info.
    #
    # INPUT:        msg            -> The message to print.
    # ----------------------------------------------------------------------
    def message(self, msg):
        log(f'[{self.name}]{self.tabs}[MESSAGE] {msg}', 2)

        print(f"\x1B[90m[\x1B[93m{self.name}\x1B[90m]{self.tabs}" + \
              f"[\x1B[34mMESSAGE\x1B[90m]\x1B[0m {msg}")

    # ----------------------------------------------------------------------
    # DESCRIPTION:  Prints a message made to display a warning.
    #
    # INPUT:        msg            -> The message to print.
    # ----------------------------------------------------------------------
    def warning(self, msg):
        log(f'[{self.name}]{self.tabs}[WARNING] {msg}', 3)

        print(f"\x1B[90m[\x1B[93m{self.name}\x1B[90m]{self.tabs}" + \
              f"[\x1B[33mWARNING\x1B[90m]\x1B[0m {msg}")

    # ----------------------------------------------------------------------
    # DESCRIPTION:  Prints a message made to display general info.
    #
    # INPUT:        msg            -> The message to print.
    #               is_fatal       -> Is the error a fatal one? Defaults to
    #                                 false if not specified.
    # ----------------------------------------------------------------------
    def error(self, msg, is_fatal=False):
        # In what world would this happen? Paranoia is the only reason why
        # this sanity check even exists in the first place.
        if type(is_fatal) != bool:
            is_fatal = False

        # I don't like having to fold my code like this.
        log(f'[{self.name}]{self.tabs}[' + 
              ('FATAL' if is_fatal else 'ERROR') + f']   {msg}', 
              5 if is_fatal else 4)

        print(f"\x1B[90m[\x1B[93m{self.name}\x1B[90m]{self.tabs}" + 
              "[\x1B[31m" + ("FATAL" if is_fatal else "ERROR") + 
              f"\x1B[90m]\x1B[0m   {msg}")
    
        # Dirty hack
        if is_fatal:
            exit()

    # ----------------------------------------------------------------------
    # DESCRIPTION:  Prints a message made to display general debug info.
    #
    # INPUT:        msg            -> The message to print.
    # ----------------------------------------------------------------------
    def debug(self, msg):
        log(f'[{self.name}]{self.tabs}[DEBUG] {msg}', 1)

        print(f"\x1B[90m[\x1B[93m{self.name}\x1B[90m]{self.tabs}" + \
              f"[\x1B[33mDEBUG\x1B[90m]\x1B[0m   {msg}")
