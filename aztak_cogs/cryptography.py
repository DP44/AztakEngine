import asyncio
import discord.utils
import bot_functions as bf
from discord.ext import tasks, commands

# --------------------------------------------------------------------------
# COG:          A cog responsible for handling crypto related commands.
# --------------------------------------------------------------------------
class Cryptography(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------
    # COMMAND:      CRC17 encode a string.
    #
    # INPUT:        data            -> The data to encode.
    # ----------------------------------------------------------------------
    @commands.command(name="crc17", brief='CRC17 encode a string.')
    async def crc17(self, ctx, data):
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

    # ----------------------------------------------------------------------
    # COMMAND:      Base64 encode a string.
    #
    # INPUT:        string          -> The string to encode.
    # ----------------------------------------------------------------------
    @commands.command(name='b64encode', brief='Base64 encode a string.')
    async def b64encode(self, ctx, string):
        try:
            msg = bf.box(
                f"Base64 encode", 
                f"Input: {string}\n" + 
                f"Output: " + 
                f"{bf.base64(string.encode(), decode=False).decode()}"
            )

            await ctx.send(f'```{msg}```')
        except Exception as e:
            msg = bf.box("Exception Handler", 
                         f"Exception caught in command 'b64encode'!\n" + 
                         f"Exception: {str(e)}")
            bf.log(e, level=40)
            await ctx.send(f"```{msg}```")

    # ----------------------------------------------------------------------
    # COMMAND:      Base64 decode a string.
    #
    # INPUT:        string          -> The string to decode.
    # ----------------------------------------------------------------------
    @commands.command(name='b64decode', brief='Base64 decode a string.')
    async def b64decode(self, ctx, string):
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

    # ----------------------------------------------------------------------
    # COMMAND:      Cryptocurrency exchange.
    #
    # INPUT:        value           -> The current crypto amount.
    #               current_type    -> Current currency to compare.
    #               target_type     -> Target currency to compare.
    # ----------------------------------------------------------------------
    @commands.command(name='exchange', brief='Check crypto exchange rates.')
    async def exchange(self, ctx, value, current_type, target_type):
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
