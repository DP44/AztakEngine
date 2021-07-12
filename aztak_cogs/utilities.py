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

    # ----------------------------------------------------------------------
    # COMMAND:      Converts an argument into bytes
    #
    # INPUT:        data            -> The data to convert.
    #               byteorder       -> The byte order of the data.
    # ----------------------------------------------------------------------
    @commands.command(name='tobytes', 
                      brief='Converts data given into bytes.')
    async def tobytes(self, ctx, data, byteorder='little'):
        try:
            byteflag = {
                'little': '<', 
                'big': '>', 
                'network': '!'
            }[byteorder]

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
                    as_bytes = bf.byte_conversion(float(data), 
                                                  f"{byteflag}f", 
                                                  encode=True)
                    selected_flag = 'f'
                except Exception:
                    as_bytes = bf.byte_conversion(float(data), 
                                                  f"{byteflag}d", 
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

            formatted = \
                str(as_bytes).replace("bytearray(b'", '').split("')")[0]
            
            msg = bf.box(
                "Byte Conversion", 
                f"Input: {data}\n " + 
                f"Output ({ctypes[selected_flag]}): {str(formatted)}"
            )

            if len(msg) < 2000:
                await ctx.send(f"```{msg}```")
            else:
                msg = bf.box(
                    "byte conversion", 
                    f"Max Length Exceeded\n" + 
                    f"Input: {data}\nOutput: {bf.content_upload(msg)}"
                )
                
                await ctx.send(f"```{msg}```")
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'tobytes'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")