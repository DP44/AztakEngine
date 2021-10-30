import asyncio
import requests
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling utility commands.
# --------------------------------------------------------------------------
class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------
    # COMMAND:      Get information on a host.
    #
    # INPUT:        addr            -> The address to check.
    # ----------------------------------------------------------------------
    @commands.command(name='ipinfo', 
                      brief='Prints info about an ip address.')
    async def ipinfo(self, ctx, addr):
        try:
            # TODO: Allow the user to specify the filters to search 
            #       for and change the output accordingly.
            response = bf.get_address_info(addr)

            if response[0] == "fail":
                await ctx.send(f"Query failed! (Recieved {response[1]})")
                return

            if response[0] == "success":
                # TODO: reformat this code, it's disgusting to look at.
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